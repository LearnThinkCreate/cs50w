// Checking if there is a value in local storage for the counter
if (!localStorage.getItem('counter')) {
    // If there's not, then initializing the value to 0
    localStorage.setItem('counter', 0);
}

function count() {
    // Getting the current value of the counter from local storage
    let counter = localStorage.getItem('counter');
    // Performing some operation
    counter ++;
    document.querySelector('h1').innerHTML = counter;
    // Updating loacl storage with the the new value
    localStorage.setItem('counter', counter);

    // Adding a template literal
    // if (counter % 10 === 0) {
    //     alert(`Couny is now ${counter}`);
    // }
}
document.addEventListener('DOMContentLoaded', () => {
    // Setting the inital value of the header to be the value of the counter in local storage
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick = count;

    // running the count function every 1 second
    // setInterval(count, 1000);
})