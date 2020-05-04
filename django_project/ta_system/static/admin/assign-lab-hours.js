import * as utils from '../ta_system/lab-hour-utils.js';
import * as settings from '../ta_system/lab-hour-settings.js';

function getConstraints(semester) {
    return utils.getLabHourData({
        endpoint: `get_lab_hour_constraints?semester=${semester}`,
        defaultValue: false
    });
}

function getPreferences(semester, eagleId) {
    return utils.getLabHourData({
        endpoint: 'get_lab_hour_preferences' +
                  `?semester=${semester}&eagle_id=${eagleId}`,
        defaultValue: false
    });
}

function getAllAssignments(semester) {
    return utils.getLabHourData({
        endpoint: `get_lab_hour_assignments?semester=${semester}`,
        defaultValue: ''
    });
}

async function getApplicants(semester) {
    const res = await fetch(`get_applicants?semester=${semester}`);
    const data = await res.json();
    if (data) return data;
    return {};
}

function getSortedEagleIds(tas) {
    const taPairs = Object.keys(tas).map(id => [id, tas[id]]);
    const sortedTaPairs = taPairs.sort((ta1, ta2) => {
        const lastName1 = ta1[1].split(' ')[1];
        const lastName2 = ta2[1].split(' ')[1];
        return lastName1.toUpperCase().localeCompare(lastName2.toUpperCase());
    });
    return sortedTaPairs.map(taPair => taPair[0]);
}

function getAssignment(assignments, eagleId) {
    return assignments.map(row => row.map(id => id == eagleId));
}

export async function renderLabHourAssignmentForm() {
    const semester = document.querySelector('#lab-hour-semester').value;
    const tas = JSON.parse(document.querySelector('#lab-hour-tas').value);
    const eagleIds = getSortedEagleIds(tas);
    const constraints = await getConstraints(semester);
    const assignments = await getAllAssignments(semester);
    const [startHour, endHour] = utils.getStartAndEndHour(constraints);
    const numHoursInDay = endHour - startHour;
    const numColumns = settings.daysOpen.length;
    const numRows = numHoursInDay * settings.numSlotsInHour;

    let preferences = await getPreferences(semester, eagleIds[0]);
    let selected = getAssignment(assignments, eagleIds[0]);
    let fromCoordinates = {row: 0, col: 0};
    let toCoordinates = {row: 0, col: 0};
    let mouseDown = false;
    let shouldSelect = true;

    function LabHourAssignmentForm() {
        return `
        ${Header()}
        <div id="lab-hour-assignment-form">
            <div class="left-assignment-grid">
                ${LabHourGrid(AssignGridItems, AssignFooter)}
            </div>
            <div class="right-assignment-grid">
                ${LabHourGrid(ViewAssignedGridItems, ViewAssignedFooter)}
            </div>
        </div>
        `;
    }

    function Header() {
        const options = eagleIds.map(eagleId =>
            `<option value="${eagleId}">${tas[eagleId]}</option>`
        ).join('');

        return `
        <header id="assignment-grid-header">
            <div id="left-grid-header">
                <div id="left-grid-header-content">
                    <label>Teaching Assistant:</label>
                    <select id="select-ta">
                        ${options}
                    </select>
                </div>
            </div>
            <div id="right-grid-header">
            </div>
        </header>
        `;
    }

    function LabHourGrid(GridItems, Footer) {
        const numLetters = utils.getNumColHeaderLetters(window);
        return `
        <div class="col-headers flex">
            ${ColumnHeaders(settings.daysOpen, numLetters)}
        </div>
        <div class="flex">
            ${GridItems(numRows, numColumns)}
            <div class="row-headers">
                ${RowHeaders(startHour, endHour)}
            </div>
        </div>
        ${Footer()}
        `;
    }

    function ColumnHeaders(daysOpen, numLetters) {
        return daysOpen.map(day =>
            `<span class="col-header">${day.substring(0, numLetters)}</span>`
        ).join('');
    }

    function AssignGridItems(numRows, numColumns) {
        let gridItems = '';
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numColumns; col++) {
                const adjustedRow = row + (startHour * settings.numSlotsInHour);
                const id = utils.getId(adjustedRow, col);
                const isOpen = constraints[adjustedRow][col];
                const isAvailable = preferences[adjustedRow][col];
                const isAssigned = assignments[adjustedRow][col];
                const isSelected = selected[adjustedRow][col];
                const isHour = (row + 1) % settings.numSlotsInHour == 0;
                let className = "grid-item";
                if (!isHour)
                    className += ' non-hour';
                if (!isOpen)
                    className += ' closed';
                if (!isAvailable || (isAssigned && !isSelected))
                    className += ' unavailable';
                if (isOpen && isAvailable && isSelected)
                    className += ' selected';
                gridItems += `<div id="${id}" class="${className}"></div>`;
            }
        }
        const style = utils.getLabHourGridStyle(numColumns, numRows);
        return `
        <div class="grid-container" style="${style}">
            ${gridItems}
        </div>
        `;
    }

    function ViewAssignedGridItems(numRows, numColumns) {
        let gridItems = '';
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numColumns; col++) {
                const adjustedRow = row + (startHour * settings.numSlotsInHour);
                const id = utils.getId(adjustedRow, col);
                const isOpen = constraints[adjustedRow][col];
                const isAssigned = assignments[adjustedRow][col];
                const isHour = (row + 1) % settings.numSlotsInHour == 0;
                let className = "read-only-grid-item";
                if (!isHour)
                    className += ' non-hour';
                if (!isOpen)
                    className += ' closed';
                if (isOpen && isAssigned)
                    className += ' selected';
                gridItems += `<div id="${id}" class="${className}"></div>`;
            }
        }
        const style = utils.getLabHourGridStyle(numColumns, numRows);
        return `
        <div class="read-only-grid-container" style="${style}">
            ${gridItems}
        </div>
        `;
    }

    function RowHeaders(startHour, endHour) {
        const times = utils.generateTimes(startHour, endHour);
        return times.map(time => {
            const height = settings.rowHeight * settings.numSlotsInHour;
            return `<div class="row-header" style="height: ${height}px">${time}</div>`
        }).join('');
    }

    function AssignFooter() {
        return `
        <div class="footer">
            <button id="assign-button" type="button">Assign</button>
            <div class="legend flex">
                <div id="legend-closed" class="legend-column">
                    <div class="legend-desc">Closed</div>
                    <div class="legend-item closed"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-busy" class="legend-desc">N/A</div>
                    <div class="legend-item unavailable"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-free" class="legend-desc">Free</div>
                    <div class="legend-item"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-assigned" class="legend-desc">Assigned</div>
                    <div class="legend-item selected"></div>
                </div>
            </div>
        </div>
        `;
    }

    function ViewAssignedFooter() {
        return `
        <div class="footer">
            <input type="submit" id="lab-hour-submit-button" class="btn btn-outline-info"/>
            <div class="legend flex">
                <div id="legend-closed" class="legend-column">
                    <div class="legend-desc">Closed</div>
                    <div class="legend-item closed"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-free" class="legend-desc">Unassigned</div>
                    <div class="legend-item"></div>
                </div>
                <div class="legend-column">
                    <div id="legend-desc-assigned" class="legend-desc">Assigned</div>
                    <div class="legend-item selected"></div>
                </div>
            </div>
        </div>
        `;
    }

    function selectFromHere(e) {
        e.preventDefault();
        const {row, col} = utils.getRowAndCol(e.target.id);
        const isOpen = constraints[row][col];
        const isAvailable = preferences[row][col];
        if (!isOpen || !isAvailable) return;
        const isSelected = selected[row][col];
        shouldSelect = !isSelected;
        toggleSelection(row, col, !isSelected);
        fromCoordinates = {row, col};
        mouseDown = true;
    }

    function toggleSelection(row, col, shouldSelectThisElement) {
        const isOpen = constraints[row][col];
        const isAvailable = preferences[row][col];
        if (!isOpen || !isAvailable) return;
        const element = utils.getElement(row, col);
        const isSelected = selected[row][col];
        selected[row][col] = shouldSelectThisElement;
        if (!isSelected && shouldSelectThisElement)
            element.className += ' selected';
        else if (isSelected && !shouldSelectThisElement)
            element.className = utils.rstrip(element.className, ' selected');
    }

    function selectToHere(e) {
        if (!mouseDown) return;
        e.preventDefault();
        let {row: rowTo, col: colTo} = toCoordinates;
        const isGridCell = e.target.className.includes('grid-item');
        if (isGridCell) toCoordinates = utils.getRowAndCol(e.target.id);
        toggleFromTo(toggleSelection);
        mouseDown = false;
    }

    function toggleFromTo(toggle) {
        const {row: rowFrom, col: colFrom} = fromCoordinates;
        const {row: rowTo, col: colTo} = toCoordinates;

        // up and left
        for (let col = colFrom; col >= colTo; col--) {
            for (let row = rowFrom; row >= rowTo; row--) {
                toggle(row, col, shouldSelect);
            }
        }
        // up and right
        for (let col = colFrom; col <= colTo; col++) {
            for (let row = rowFrom; row >= rowTo; row--) {
                toggle(row, col, shouldSelect);
            }
        }
        // down and left
        for (let col = colFrom; col >= colTo; col--) {
            for (let row = rowFrom; row <= rowTo; row++) {
                toggle(row, col, shouldSelect);
            }
        }
        // down and right
        for (let col = colFrom; col <= colTo; col++) {
            for (let row = rowFrom; row <= rowTo; row++) {
                toggle(row, col, shouldSelect);
            }
        }
    }

    function highlightToHere(e) {
        if (!mouseDown) return;
        e.preventDefault();
        toCoordinates = utils.getRowAndCol(e.target.id);
        toggleHighlightFromTo();
    }

    function toggleHighlightFromTo() {
        toggleFromTo(toggleHighlight);

        // undo toggleHighlights from past mouseenter events for
        // all grid cells not within the new from - to rectangular plane
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numColumns; col++) {
                const isOpen = constraints[row][col];
                const isAvailable = preferences[row][col];
                if (isOpen && isAvailable && !isWithinFromToPlane(row, col)) {
                    const element = utils.getElement(row, col);
                    const isHighlighted = element.className.includes('selected');
                    const isSelected = selected[row][col];
                    if (isSelected && !isHighlighted)
                         element.className += ' selected';
                    else if (!isSelected && isHighlighted)
                        element.className = utils.rstrip(element.className, ' selected');
                }
            }
        }
    }

    function toggleHighlight(row, col, shouldHighlightThisElement) {
        const isOpen = constraints[row][col];
        const isAvailable = preferences[row][col];
        if (!isOpen || !isAvailable) return;
        const element = utils.getElement(row, col);
        const isHighlighted = element.className.includes('selected');
        if (!isHighlighted && shouldHighlightThisElement)
            element.className += ' selected';
        else if (isHighlighted && !shouldHighlightThisElement)
            element.className = utils.rstrip(element.className, ' selected');
    }

    function isWithinFromToPlane(row, col) {
        const {row: rowFrom, col: colFrom} = fromCoordinates;
        const {row: rowTo, col: colTo} = toCoordinates;

        // up and left
        if (rowTo <= rowFrom && colTo <= colFrom) {
            return ((rowTo <= row) && (row <= rowFrom))
                && ((colTo <= col) && (col <= colFrom));
        }
        // up and right
        if (rowTo <= rowFrom && colFrom <= colTo) {
            return ((rowTo <= row) && (row <= rowFrom))
                && ((colFrom <= col) && (col <= colTo));
        }
        // down and left
        if (rowFrom <= rowTo && colTo <= colFrom) {
            return ((rowFrom <= row) && (row <= rowTo))
                && ((colTo <= col) && (col <= colFrom));
        }
        // down and right
        if (rowFrom <= rowTo && colFrom <= colTo) {
            return ((rowFrom <= row) && (row <= rowTo))
                && ((colFrom <= col) && (col <= colTo));
        }
    }

    function resizeColHeaders(e) {
        const colHeaders = document.querySelector('.col-headers');
        const numLetters = utils.getNumColHeaderLetters(e.target);
        colHeaders.innerHTML = ColumnHeaders(settings.daysOpen, numLetters);
    }

    function setSelectedApplicant(eagleId) {
        const selectApplicant = document.querySelector('#select-ta');
        selectApplicant.value = eagleId;
    }

    function assignHours(e) {
        const eagleId = document.querySelector('#select-ta').value;
        selected.forEach((row, rowIdx) => {
            row.forEach((isSelected, colIdx) => {
                const isAssigned = assignments[rowIdx][colIdx] == eagleId;
                if (isSelected)
                    assignments[rowIdx][colIdx] = eagleId;
                else if (!isSelected && isAssigned)
                    assignments[rowIdx][colIdx] = '';
            })
        })
        render();
        setSelectedApplicant(eagleId);
    }

    async function changeTA(e) {
        const eagleId = e.target.value;
        preferences = await getPreferences(semester, eagleId);
        selected = getAssignment(assignments, eagleId);
        render();
        setSelectedApplicant(eagleId);
    }

    function outputAssignments() {
        const labHourInput = document.querySelector('#id_lab_hour_data');
        labHourInput.value = JSON.stringify(assignments);
    }

    function render() {
        const labHourFormRoot = document.querySelector('#lab-hour-form');
        labHourFormRoot.innerHTML = LabHourAssignmentForm();
        const timeSlots = document.querySelectorAll('.grid-item');
        timeSlots.forEach(slot => {
            slot.onmousedown = selectFromHere;
            slot.onmouseenter = highlightToHere;
            slot.onmouseup = selectToHere;
        });
        const assignButton = document.querySelector('#assign-button');
        assignButton.onclick = assignHours;
        const selectTA = document.querySelector('#select-ta');
        selectTA.onchange = changeTA;
        const grid = document.querySelector('.grid-container');
        grid.oncontextmenu = e => e.preventDefault();
        window.onmouseup = selectToHere;
        window.onresize = resizeColHeaders;
        document.querySelector('#id_semester').value = semester;
        console.log(semester);
        outputAssignments();
    }

    render();
}

renderLabHourAssignmentForm();
