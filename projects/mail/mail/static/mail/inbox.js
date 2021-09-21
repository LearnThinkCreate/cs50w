document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Add send/compose handling
  sendEmailHandling();
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

//  Send api call to get the respective mailbox
fetch(`/emails/${mailbox}`)
.then (response => response.json())
.then (emails => {
  // Loading all the emails
  emails.forEach(add_email);
})
};

function add_email(contents) {
  // Creating the bootstrap container
  const container = document.createElement('div');
  container.className = 'row';

  // Seeting if the email has been read 
  if (contents['read']) {
    container.className += ' email-read';
  }

  let email_contents = {
    "sender":{
      "type":"sender"
    },
    "subject":{
      "type":"subject"
    },
    "timestamp":{
      "type":"subject"
    }
  };

  // Creating the 
  for (email in email_contents) {
    console.log(typeof(document.createElement('div')));
    email['div'] = document.createElement('div');
    console.log(typeof(email['div']))
    if (email[0] === "subject") {
      email['div'].className = 'col-6 email-inbox'; 
    } else {
      email['div'].className = 'col-3 email-inbox';
    }

    email['div'].innerHTML = contents[email['type']];

    container.appendChild(email['div'])
  }
  // Creating the email contents 
  // const sender = document.createElement('div');
  // const subject = document.createElement('div');
  // const timestamp = document.createElement('div');

  // // Styling the divs 
  // sender.className = 'col-3 email-inbox';
  // subject.className = 'col-6 email-inbox';
  // timestamp.className = 'col-3 email-inbox'

  // // Adding the email contents
  // sender.innerHTML = contents["sender"];
  // subject.innerHTML = contents['subject'];
  // timestamp.innerHTML = contents['timestamp'];

  // // Appending the contents to the row container 
  // container.appendChild(sender);
  // container.appendChild(subject);
  // container.appendChild(timestamp);

  // Appending to the emails view for now
  document.querySelector('#emails-view').append(container);
};

function sendEmailHandling() {
  document.querySelector('#compose-form').addEventListener("submit", (event) => {
    // Force not to relod
    event.preventDefault();

    // Post the email to the server
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    // converting the response to json
    .then(response => response.json())
    // Showing the response or throwing an error
    .then(result => {
      // Logging the results
      console.log(result);
      // Throw an error if there is one
      if (Object.keys(result)[0] === "error") {
        throw new Error(result.error);
      }
      // Go to inbox and show success message
      else {
        load_mailbox('inbox');
        alert(result.message);
      }       
    })
    // Handle the error 
    .catch(error => {
      alert(error);
    })
  })
}