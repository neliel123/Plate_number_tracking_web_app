// Establish a Socket.IO connection
// var socket = io.connect();
// var socket = io();
var socket = io("plate-number-tracking-web-app.onrender.com");

// Listen for the 'updateMotorcycleTracking' event
socket.on("updateMotorcycleTracking", function (msg) {
    console.log(msg);
    if (msg.isError === "false") {
        // Update the current motorcycle details
        updateCurrentMotorcycle(msg);
        // Update the last 10 motorcycles list
        updateLast10Motorcycles(msg);
        // Update the count of motorcycles detected today
        updateMotorcycleCount(msg.count);
    }
});

function updateCurrentMotorcycle(msg) {
    // Elements to update
    var latestTUPIdElem = document.getElementById("latestTUPId");
    var plateNumberElem = document.getElementById("latestPlateNumber");
    var modelElem = document.getElementById("latestModel");
    var ownerElem = document.getElementById("latestOwner");
    var sectionElem = document.getElementById("latestSection");
    var userPictureElem = document.getElementById("userPicture");

    // Update the text 
    latestTUPIdElem.textContent = msg.owner.tup_id;
    plateNumberElem.textContent = msg.plate_number;
    modelElem.textContent = msg.model;
    ownerElem.textContent = msg.owner ? `${msg.owner.first_name} ${msg.owner.last_name}` : "Unknown";
    sectionElem.textContent = msg.owner.section;

    // Update the picture URL
    if (msg.owner && msg.owner.picture_url) {
        userPictureElem.src = msg.owner.picture_url;
        userPictureElem.alt = `${msg.owner.first_name} ${msg.owner.last_name}`; // Optional: Set alt text
        userPictureElem.style.width = "300px"; // Set fixed width
        userPictureElem.style.height = "auto"; // Maintain aspect ratio
    } else {
        userPictureElem.src = ""; // Clear the image if no picture_url is provided
        userPictureElem.alt = "No picture available"; // Optional: Set alt text
    }

    // Add animation classes
    addAnimation(plateNumberElem);
    addAnimation(modelElem);
    addAnimation(ownerElem);
    addAnimation(sectionElem);
    addAnimation(userPictureElem);
}

function addAnimation(element) {
    // Add animation class (replace 'bounce' with your preferred animation)
    element.classList.add('animate__animated', 'animate__bounce');

    // Remove animation class after a set duration (optional)
    setTimeout(() => {
        element.classList.remove('animate__animated', 'animate__bounce');
    }, 1000); // Adjust duration as needed (in milliseconds)
}

function updateLast10Motorcycles(msg) {
    // Get the table body for the last 10 motorcycles
    var tableBody = document.querySelector("#plateNumberList tbody");
    
    // Insert a new row at the top
    var newRow = tableBody.insertRow(0);

    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);
    var cell5 = newRow.insertCell(4);

    // Add the content to the new cells
    cell1.textContent = 1; // Serial number for the latest entry
    cell2.textContent = msg.plate_number;
    cell3.textContent = msg.model;
    cell4.textContent = msg.owner ? `${msg.owner.first_name} ${msg.owner.last_name}` : "Unknown";
    cell5.textContent = msg.owner ? msg.owner.section : "Unknown";

    // Update serial numbers for existing rows
    for (var i = 1; i < tableBody.rows.length; i++) {
        tableBody.rows[i].cells[0].textContent = i + 1;
    }

    // Limit the table to 10 rows
    if (tableBody.rows.length > 10) {
        tableBody.deleteRow(10);
    }
}

function updateMotorcycleCount(count) {
    // Update the count of motorcycles detected today
    document.getElementById("numberOfMotorcycles").textContent = count;
}
