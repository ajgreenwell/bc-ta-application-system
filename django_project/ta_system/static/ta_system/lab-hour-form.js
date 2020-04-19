import * as utils from './lab-hour-utils.js';
import * as settings from './lab-hour-settings.js';


export async function renderLabHourForm(props) {
    const { getConstraints, getStartingGrid, extraJS } = props;
    const constraints = await getConstraints();
    const [startHour, endHour] = utils.getStartAndEndHour(constraints);
    let selected = await getStartingGrid();
    let fromCoordinates = {row: 0, col: 0};
    let mouseDown = false;
    let shouldSelect = true;

    function LabHourGrid() {
        const numHoursInDay = endHour - startHour;
        const numColumns = settings.daysOpen.length;
        const numRows = numHoursInDay * settings.numSlotsInHour;
        const style = utils.getLabHourGridStyle(numColumns, numRows);
        const numLetters = utils.getNumColHeaderLetters(window);
        return `
            <div class="col-headers flex">
                ${ColumnHeaders(settings.daysOpen, numLetters)}
            </div>
            <div class="flex">
                <div class="grid-container" style="${style}" >
                    ${GridItems(numRows, numColumns)}
                </div>
                <div class="row-headers">
                    ${RowHeaders(startHour, endHour)}
                </div>
            </div>
            <div class="flex">
                <input type="submit" id="lab-hour-submit-button" class="btn btn-outline-info btn-red" />
                ${Legend()}
            </div>
        `;
    }

    function ColumnHeaders(daysOpen, numLetters) {
        return daysOpen.map(day =>
            `<span class="col-header">${day.substring(0, numLetters)}</span>`
        ).join('');
    }

    function GridItems(numRows, numColumns) {
        let gridItems = '';
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numColumns; col++) {
                const adjustedRow = row + (startHour * settings.numSlotsInHour);
                const id = utils.getId(adjustedRow, col);
                const isOpen = constraints[adjustedRow][col];
                const isSelected = selected[adjustedRow][col];
                const isHour = (row + 1) % settings.numSlotsInHour == 0;
                let className = "grid-item";
                if (!isHour)
                    className += ' non-hour';
                if (!isOpen)
                    className += ' closed';
                if (isOpen && isSelected)
                    className += ' selected';
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

    function Legend() {
        return `
            <div class="legend flex">
                <div id="legend-closed" class="legend-column">
                    <div class="legend-desc">N/A</div>
                    <div class="legend-item closed"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-busy" class="legend-desc">Busy</div>
                    <div class="legend-item"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-free" class="legend-desc">Free</div>
                    <div class="legend-item selected"></div>
                </div>
            </div>
        `;
    }

    function toggleSelectionFromTo(fromCoordinates, toCoordinates) {
        const {row: rowFrom, col: colFrom} = fromCoordinates;
        const {row: rowTo, col: colTo} = toCoordinates;

        // up and left
        for (let col = colFrom; col >= colTo; col--) {
            for (let row = rowFrom; row >= rowTo; row--) {
                toggleSelection(row, col, shouldSelect);
            }
        }
        // up and right
        for (let col = colFrom; col <= colTo; col++) {
            for (let row = rowFrom; row >= rowTo; row--) {
                toggleSelection(row, col, shouldSelect);
            }
        }
        // down and left
        for (let col = colFrom; col >= colTo; col--) {
            for (let row = rowFrom; row <= rowTo; row++) {
                toggleSelection(row, col, shouldSelect);
            }
        }
        // down and right
        for (let col = colFrom; col <= colTo; col++) {
            for (let row = rowFrom; row <= rowTo; row++) {
                toggleSelection(row, col, shouldSelect);
            }
        }
    }

    function toggleSelection(row, col, shouldSelectThisElement) {
        const isClosed = !constraints[row][col];
        if (isClosed) return;
        const id = utils.getId(row, col);
        const element = document.getElementById(id);
        const isSelected = selected[row][col];
        selected[row][col] = shouldSelectThisElement;
        if (!isSelected && shouldSelectThisElement)
            element.className += ' selected';
        else if (isSelected && !shouldSelectThisElement)
            element.className = utils.rstrip(element.className, ' selected');
    }

    function selectFromHere(e) {
        const [row, col] = utils.getRowAndCol(e.target.id);
        const isClosed = !constraints[row][col];
        if (isClosed) return;
        mouseDown = true;
        const isSelected = selected[row][col];
        if (isSelected) {
            toggleSelection(row, col, !isSelected);
            shouldSelect = false;
        } else {
            toggleSelection(row, col, !isSelected);
            shouldSelect = true;
        }
        fromCoordinates = {row, col};
        outputSelected();
    }

    function selectToHere(e) {
        if (!mouseDown) return;
        const [rowTo, colTo] = utils.getRowAndCol(e.target.id);
        const isClosed = !constraints[rowTo][colTo];
        if (isClosed) return;
        const toCoordinates = {row: rowTo, col: colTo};
        toggleSelectionFromTo(fromCoordinates, toCoordinates);
        outputSelected();
    }

    function stopSelecting(e) {
        mouseDown = false;
    }

    function resizeColHeaders(e) {
        const colHeaders = document.querySelector('.col-headers');
        const numLetters = utils.getNumColHeaderLetters(e.target);
        colHeaders.innerHTML = ColumnHeaders(settings.daysOpen, numLetters);
    }

    function outputSelected() {
        const labHourInput = document.querySelector('#id_lab_hour_data');
        labHourInput.value = JSON.stringify(selected);
    }

    const labHourFormRoot = document.querySelector('#lab-hour-form');
    if (!labHourFormRoot) return;
    labHourFormRoot.innerHTML = LabHourGrid();
    const timeSlots = document.querySelectorAll('.grid-item');
    timeSlots.forEach(slot => {
        slot.onmousedown = selectFromHere;
        slot.onmouseenter = selectToHere;
    });
    window.onmouseup = stopSelecting;
    window.onresize = resizeColHeaders;
    outputSelected();
    if (extraJS) extraJS();
}
