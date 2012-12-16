/*global require console phantom */
// First argument to the script is the ID of the event
var casper = require('casper').create(),
    utils = require('utils'),
    rsvps = null,
    eventId, url;

phantom.onError = function(msg, trace) {
    console.error(msg);
    casper.exit(1);
};

if (casper.cli.args.length !== 1) {
    throw new Error("You have to pass a Google+ event id as first argument");
} else {
    eventId = casper.cli.args[0];
    url = "https://plus.google.com/events/" + eventId + "?hl=en";
}

casper.start().thenOpen(url, {method:'get', headers:{'Accept-Language': 'en'}}, function(status) {
    if (status === 'fail') {
        throw new Error("Failed to fetch page");
    }
    rsvps = this.evaluate(function() {
        function getCollection(title) {
            if (title.indexOf("Going") === 0) {
                return 'coming';
            }
            if (title.indexOf("Maybe") === 0) {
                return 'maybe';
            }
            return 'unknown';
        }
        var result = {
                coming: [],
                maybe: [],
                not_coming: [],
                unknown: []
            },
            peopleCollections = document.querySelectorAll('div.gRa'), // [0].querySelectorAll('li .cua a')
            num = peopleCollections.length,
            people, numPeople, title, i, j, person, name, id, cname;
        for (i = 0; i < num; i++) {
            title = peopleCollections[i].getElementsByTagName("h3")[0].textContent;
            cname = getCollection(title);
            people = peopleCollections[i].querySelectorAll('li .cua a');
            numPeople = people.length;
            for (j = 0; j < numPeople; j++) {
                person = people[j];
                name = person.textContent;
                id = person.getAttribute("href").substring(2);
                result[cname].push({'name': name, 'id': id});
            }
        }
        return result;
    });
    console.log(JSON.stringify(rsvps, null, "    "));
    casper.exit(0);
});
casper.run();
