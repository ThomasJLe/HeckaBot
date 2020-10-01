const Discord = require("discord.js");
const config = require("./config.json");
const client = new Discord.Client();
client.login(config.token);

// Globols
var reminders = [];
var channel = client.channels.cache.get('701608486517211169');

// Ready Event
client.on('ready',() => {
	console.log('logged in!');
});

// Class Definition
class Reminder {
	constructor(date, time, description) {
		this.date = date;
		this.time = time;
		this.description = description;

	}
	showReminder(){
		var channel = client.channels.cache.get('701608486517211169');
		channel.send(this.description + " Date: " + this.date + " Time: " + this.time);
	}
	printAll() {
		var channel = client.channels.cache.get('701608486517211169');
		for (var i = 0; i < reminders.length; i++)
		{
			channel.send(this.description + " Date: " + this.date + " Time: " + this.time + '\n');
		}
	}
	addTo() {
		reminders.push(this);
	}
}

// Message Events
/*
	Reminder Command structure
	!setReminder ddmmyyyy 2300 description
	1. Class 'Reminder' and Data Structure of Reminder to hold inputs
	3. Create setInterval or setTimeout event for reminder?
	Test general chat channel ID = '701608486517211169'
*/
client.on('message', msg => {
		// Command prefix
    const prefix = '!';

    if (msg.content.startsWith(prefix)) {
				// Arguments are split and stored in args[]
				// Command is isolated
				var args = msg.content.slice(prefix.length).trim().split(' ');
				var command = args.shift();

				if (command === 'setReminder') {
		  			// Create a new reminder object
		  			const newReminder = new Reminder(args[0], args[1], args[2]);
						// Display Result - Add to Array[Reminders]
						newReminder.showReminder();
						newReminder.addTo();
					}
				else if (command === 'showAllReminders') {
						const newReminder = new Reminder();
						newReminder.printAll();
					}
   		}
});
