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

  // Viewing email when preview is clicked on
  document.querySelectorAll('.email-preview').forEach(email => {

    // Go to email view
    email.onclick = () => {
      console.log(email.dataset.emailID);
      viewEmail(email.dataset.emailID);
    }
  })
});


// ------ Shows mailbox ------
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

//  Send api call to get the respective mailbox
fetch(`/emails/${mailbox}`)
.then (response => response.json())
.then (emails => {
  // Loading all the emails
  emails.forEach(add_email);
});
};
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

// ------ Shows compose email view ------ 
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

// ------ Creates new email block for mailbox view  ------ 
function add_email(contents) {

  // Creating the bootstrap container
  const container = document.createElement('div');
  container.className = 'row email-preview';

  // Storing the email id in the div
  container.dataset.emailID = contents['id']

  container.addEventListener('click', () => {
    viewEmail(container.dataset.emailID);
  }); 

  // Seeing if the email has been read 
  if (contents['read']) {
    // appending email read to the existing class names
    container.className += ' email-read';
  }

  // array for the different components of inbox element
  let content_types = [
    'sender', 'subject', 'timestamp'
  ]
  
  // Adding emails to the inbox
  for (i in content_types) {

    // Styling each type of the email preview in a seperate div
    let type = content_types[i]
    let new_div = document.createElement('div');

    // Giving the div a class
    if (type === "subject") {
      new_div.className = 'col-6 email-inbox';
    } else  {
      new_div.className = 'col-3 email-inbox'; 
    }

    // Attatching contents 
    new_div.innerHTML = contents[type];

    // Appending new div to the boostrap container
    container.appendChild(new_div)
  }

  // Appending the bootstrap container to the email views div
  document.querySelector('#emails-view').append(container);
};
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

// ------ Sends email ------ 
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
};
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

// ------ Shows email's details ------
function viewEmail(emailID) {

    // Show the mailbox and hide other views
    // document.querySelector('#emails-view').style.display = 'none';
    // document.querySelector('#compose-view').style.display = 'none';
    // document.querySelector('#view-email').styel.display = 'block';
    
  console.log(emailID)

  //  Getting the contents of hte mail
  fetch(`/emails/${emailID}`)
  .then (response => response.json())
  .then (email => {
    // Loading all the emails
    console.log(email)
    let contents = email;
  });

  // Marking the email as read
  fetch(`/emails/${emailID}`,  {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  } )

  // Displaying the contents of the email
  

};
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 