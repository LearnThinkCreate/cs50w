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
  console.log(emails);

  const email = document.createElement('div')
  // Create a class for email divs and assign
  email.className = 'emailDiv';
  
  // 
})
}

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