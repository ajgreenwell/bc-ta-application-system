import {
    getLabHourConstraints,
    getStartAndEndHour,
    initSelectedMatrix
} from './utils.js';

import {
    numSlotsInHour,
    rowHeight,
    daysOpen
} from './cs-lab-hour-settings.js';

const constraints = getLabHourConstraints();
const [startHour, endHour] = getStartAndEndHour(constraints);

let mouseDown = false;
let isSelected = initSelectedMatrix(constraints);

function renderLabHourForm() {
    document.querySelector('#cs-lab-hour-form').innerHTML = LabHourGrid();
    const button = document.querySelector('#cs-lab-hour-submit-button');
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
    const numColumns = daysOpen.length;
    const numRows = numHoursInDay * numSlotsInHour;
    return `
        <div class="col-headers flex">
            ${ColumnHeaders(daysOpen)}
        </div>
        <div class="flex">
            <div class="grid-container" style="${getLabHourGridStyle(numColumns, numRows)}" >
                ${GridItems(numRows, numColumns)}
            </div>
            <div class="row-headers">
                ${RowHeaders(startHour, endHour)}
            </div>
        </div>
        <button id="cs-lab-hour-submit-button" class="btn btn-outline-info btn-red">
            Submit
        </button>
    `;
}

function ColumnHeaders(daysOpen) {
    return daysOpen.map(day =>
        `<span class="col-header">${day.substring(0, 3)}</span>`
    ).join('');
}

function RowHeaders(startHour, endHour) {
    const times = generateTimes(startHour, endHour);
    return times.map(time => {
        const height = rowHeight * numSlotsInHour;
        return `<div class="row-header" style="height: ${height}px">${time}</div>`
    }).join('');
}

function getLabHourGridStyle(numColumns, numRows) {
    let columns = '';
    let rows = '';
    for (let col = 0; col < numColumns; col++)
        columns += 'auto ';
    for (let row = 0; row < numRows; row++)
        rows += `${rowHeight}px `;
    return `grid-template-columns: ${columns}; grid-template-rows: ${rows}`;
}

function GridItems(numRows, numColumns) {
    let gridItems = '';
    for (let row = 0; row < numRows; row++) {
        for (let col = 0; col < numColumns; col++) {
            const adjustedRow = row + (startHour * numSlotsInHour);
            const id = `row:${adjustedRow},col:${col}`;
            const isHour = (row + 1) % numSlotsInHour == 0;
            const isOpen = constraints[adjustedRow][col];
            let className = "grid-item";
            if (!isOpen) className += ' closed';
            if (!isHour) className += ' non-hour';
            gridItems += `<div id="${id}" class="${className}"></div>`;
        }
    }
    return gridItems;
}

function generateTimes(startHour, endHour) {
    let times = [];
    for (let hour = startHour; hour <= endHour; hour++) {
        let time = convertFromMillitary(hour);
        times.push(time);
    }
    return times;
}

function convertFromMillitary(hour) {
    let time = '';
    if (hour > 12)
        time = `${hour - 12}:00 PM`;
    else if (hour == 12)
        time = `${hour}:00 PM`;
    else {
        hour = hour == 0 ? 12 : hour;
        time = `${hour}:00 AM`;
    }
    return time;
}

function submitApplicationForm() {
    console.log('submitted application form');
}

function selectFromHere(e) {
    mouseDown = true;
    const className = e.target.className;
    const [row, col] = getRowAndColFromId(e.target.id);
    const isClosed = !constraints[row][col];
    if (isClosed) return;
    if (className.includes('selected')) {
        e.target.className = rstrip(className, ' selected');
        isSelected[row][col] = false;
        console.log(isSelected);
    } else {
        e.target.className += ' selected';
        isSelected[row][col] = true;
        console.log(isSelected);
    }
}

function selectToHere(e) {
    if (mouseDown) selectFromHere(e);
}

function stopSelecting(e) {
    mouseDown = false;
}

function getRowAndColFromId(id) {
    let [row, col] = id.split(',');
    row = row.split(':')[1];
    col = col.split(':')[1];
    return [row, col];
}

function rstrip(str, substr) {
    const index = str.indexOf(substr);
    return str.substring(0, index);
}

renderLabHourForm();
