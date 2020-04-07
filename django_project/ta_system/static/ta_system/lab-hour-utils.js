import { numSlotsInHour, rowHeight } from './lab-hour-settings.js';

export function getLabHourConstraints() {
    const falseConstraintRow = [false, false, false, false, false, false, false];
    const trueConstraintRow = [false, true, true, true, true, true, false];
    const constraints = [];
    for (let i = 0; i < 38; i++)
        constraints.push(falseConstraintRow);
    for (let j = 0; j < 32; j++)
        constraints.push(trueConstraintRow);
    for (let k = 0; k < 26; k++)
        constraints.push(falseConstraintRow);
    return constraints;
}

export function getStartAndEndHour(constraints) {
    let [startRow, endRow] = [0, constraints.length - 1];
    let [isStart, isEnd] = [false, false];
    while (startRow < endRow) {
        isStart = constraints[startRow].includes(true);
        if (isStart) break;
        startRow++;
    }
    while (startRow < endRow) {
        isEnd = constraints[endRow].includes(true);
        if (isEnd) break;
        endRow--;
    }
    if (endRow <= startRow)
        return [0, constraints.length];
    const startHour = Math.floor(startRow / numSlotsInHour);
    const endHour = Math.ceil((endRow + 1) / numSlotsInHour);
    return [startHour, endHour];
}

export function initSelectedMatrix(constraints) {
    let isSelected = [];
    constraints.forEach(row => {
        let initRow = row.map( _ => false);
        isSelected.push(initRow);
    });
    return isSelected;
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
    return [row, col];
}

export function rstrip(str, substr) {
    const index = str.indexOf(substr);
    return str.substring(0, index);
}
