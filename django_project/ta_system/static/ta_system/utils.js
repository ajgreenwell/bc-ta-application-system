import { numSlotsInHour } from './cs-lab-hour-settings.js';

export function getLabHourConstraints() {
    const falseConstraintRow = [false, false, false, false, false, false, false];
    const trueConstraintRow = [false, true, true, false, true, true, false];
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