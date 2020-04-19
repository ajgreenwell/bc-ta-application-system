import { numSlotsInHour, rowHeight } from './lab-hour-settings.js';

export function initLabHourGrid(value) {
    let grid = [];
    for (let row = 0; row < 24 * numSlotsInHour; row++) {
        let row = [];
        for (let col = 0; col < 7; col++)
            row.push(value);
        grid.push(row);
    }
    return grid;
}

export async function getLabHourConstraints(endpoint, defaultValue) {
    const res = await fetch(endpoint);
    const data = await res.json();
    if (data && data.length) return data;
    return initLabHourGrid(defaultValue);
}

export async function getLabHourPreferences() {
    const res = await fetch('/get_lab_hour_preferences/');
    const data = await res.json();
    if (data && data.length) return data;
    return initLabHourGrid(false);
}

export function getStartAndEndHour(constraints) {
    let [startRow, endRow] = [0, constraints.length - 1];
    let [isStart, isEnd] = [false, false];
    while (startRow <= endRow) {
        isStart = constraints[startRow].includes(true);
        if (isStart) break;
        startRow++;
    }
    while (startRow <= endRow) {
        isEnd = constraints[endRow].includes(true);
        if (isEnd) break;
        endRow--;
    }
    if (endRow < startRow)
        return [0, constraints.length - 1];
    const startHour = Math.floor(startRow / numSlotsInHour);
    const endHour = Math.ceil((endRow + 1) / numSlotsInHour);
    return [startHour, endHour];
}

export function getNumColHeaderLetters(windowObj) {
    return windowObj.screen.width < 400 ? 2 : 3;
}

export function getLabHourGridStyle(numColumns, numRows) {
    let columns = '';
    let rows = '';
    for (let col = 0; col < numColumns; col++)
        columns += 'auto ';
    for (let row = 0; row < numRows; row++)
        rows += `${rowHeight}px `;
    return `grid-template-columns: ${columns}; grid-template-rows: ${rows}`;
}

export function generateTimes(startHour, endHour) {
    let times = [];
    for (let hour = startHour; hour <= endHour; hour++) {
        let time = convertFromMillitary(hour);
        times.push(time);
    }
    return times;
}

export function convertFromMillitary(hour) {
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

export function getId(row, col) {
    return `row:${row},col:${col}`;
}

export function getRowAndCol(id) {
    let [row, col] = id.split(',');
    row = row.split(':')[1];
    col = col.split(':')[1];
    return [parseInt(row), parseInt(col)];
}

export function rstrip(str, substr) {
    const index = str.indexOf(substr);
    if (index == -1) return str;
    return str.substring(0, index);
}
