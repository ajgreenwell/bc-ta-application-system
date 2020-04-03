import * as utils from './lab-hour-utils.js';
import * as settings from './lab-hour-settings.js';
import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@rc/dist/js.cookie.min.mjs';

const constraints = utils.getLabHourConstraints();
const [startHour, endHour] = utils.getStartAndEndHour(constraints);

let mouseDown = false;
let isSelected = utils.initSelectedMatrix(constraints);

function renderLabHourForm() {
    document.querySelector('#lab-hour-form').innerHTML = LabHourGrid();
    const button = document.querySelector('#lab-hour-submit-button');
    button.onclick = submitApplicationForm;
    const timeSlots = document.querySelectorAll('.grid-item');
    timeSlots.forEach(slot => {
        slot.onmousedown = selectFromHere;
        slot.onmouseover = selectToHere;
        slot.onmouseup = stopSelecting;
    });
}

function LabHourGrid() {
    const numHoursInDay = endHour - startHour;
    const numColumns = settings.daysOpen.length;
    const numRows = numHoursInDay * settings.numSlotsInHour;
    const style = utils.getLabHourGridStyle(numColumns, numRows);
    return `
        <div class="col-headers flex">
            ${ColumnHeaders(settings.daysOpen)}
        </div>
        <div class="flex">
            <div class="grid-container" style="${style}" >
                ${GridItems(numRows, numColumns)}
            </div>
            <div class="row-headers">
                ${RowHeaders(startHour, endHour)}
            </div>
        </div>
        <button id="lab-hour-submit-button" class="btn btn-outline-info btn-red">
            Submit
        </button>
    `;
}

function ColumnHeaders(daysOpen) {
    return daysOpen.map(day =>
        `<span class="col-header">${day.substring(0, 3)}</span>`
    ).join('');
}

function GridItems(numRows, numColumns) {
    let gridItems = '';
    for (let row = 0; row < numRows; row++) {
        for (let col = 0; col < numColumns; col++) {
            const adjustedRow = row + (startHour * settings.numSlotsInHour);
            const id = utils.getId(adjustedRow, col);
            const isOpen = constraints[adjustedRow][col];
            const isHour = (row + 1) % settings.numSlotsInHour == 0;
            let className = "grid-item";
            if (!isOpen) className += ' closed';
            if (!isHour) className += ' non-hour';
            gridItems += `<div id="${id}" class="${className}"></div>`;
        }
    }
    return gridItems;
}

function RowHeaders(startHour, endHour) {
    const times = utils.generateTimes(startHour, endHour);
    return times.map(time => {
        const height = settings.rowHeight * settings.numSlotsInHour;
        return `<div class="row-header" style="height: ${height}px">${time}</div>`
    }).join('');
}

function Success() {
    return `
        <h2>Success! Your Application has been submitted.</h2>
        <p>
            To edit your account info or update your CS Lab availability,
            head on over to your <a href= "/profile">profile</a> page.
        </p>
    `;
}

function submitApplicationForm() {
    const csrftoken = Cookies.get('csrftoken');
    fetch('/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ lab_hour_preferences: isSelected })
    }).then(res => {
        if (res.ok)
            window.location.href = '/';
        else console.log('Failed to save lab hour data.');
    }).catch(err =>  console.log(err));
}

function selectFromHere(e) {
    mouseDown = true;
    const className = e.target.className;
    const [row, col] = utils.getRowAndCol(e.target.id);
    const isClosed = !constraints[row][col];
    if (isClosed) return;
    if (className.includes('selected')) {
        e.target.className = utils.rstrip(className, ' selected');
        isSelected[row][col] = false;
    } else {
        e.target.className += ' selected';
        isSelected[row][col] = true;
    }
}

function selectToHere(e) {
    if (mouseDown) selectFromHere(e);
}

function stopSelecting(e) {
    mouseDown = false;
}

renderLabHourForm();
