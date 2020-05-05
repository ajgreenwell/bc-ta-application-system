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
    const taColors = JSON.parse(document.querySelector('#lab-hour-ta-colors').value);
    const eagleIds = getSortedEagleIds(tas);
    const constraints = await getConstraints(semester);
    const assignments = await getAllAssignments(semester);
    const [startHour, endHour] = utils.getStartAndEndHour(constraints);
    const numHoursInDay = endHour - startHour;
    const numColumns = settings.daysOpen.length;
    const numRows = numHoursInDay * settings.numSlotsInHour;

    let selectedEagleId = eagleIds[0];
    let preferences = await getPreferences(semester, selectedEagleId);
    let selected = getAssignment(assignments, selectedEagleId);
    let fromCoordinates = {row: 0, col: 0};
    let toCoordinates = {row: 0, col: 0};
    let mouseDown = false;
    let shouldSelect = true;

    function LabHourAssignmentForm() {
        return `
        ${Header()}
        <div id="lab-hour-assignment-form">
            <div class="left-assignment-grid">
                ${LabHourGrid(AssignGridItems)}
            </div>
            <div class="right-assignment-grid">
                ${LabHourGrid(ViewAssignedGridItems)}
            </div>
        </div>
        `;
    }

    function Header() {
        const options = eagleIds.map(eagleId =>
            `<option value="${eagleId}">${tas[parseInt(eagleId)]}</option>`
        ).join('');
        const verboseSemester = document.querySelector('#lab-hour-verbose-semester').value;
        const taLegendColumns = eagleIds.map(eagleId => {
            const name = tas[parseInt(eagleId)];
            const [r, g, b] = taColors[parseInt(eagleId)];
            const color = `rgb(${r}, ${g}, ${b})`;
            const style = `background-color: ${color}`;
            return `
            <div id="legend-column" class="legend-column">
                <div id="legend-desc-${eagleId}" class="legend-desc">${name}</div>
                <div id="legend-item-${eagleId}" class="legend-item" style="${style}"></div>
            </div>
            `;
        }).join('');


        return `
        <header id="assignment-grid-header">
            <div id="left-grid-header">
                <div id="left-grid-header-content">
                    <h2>Individual Assignments</h2>
                    <p>
                        Choose a teaching assistant from the list and modify their lab hour
                        assignments using the grid below. Each individual assignment will be
                        displayed on the "All Assignments" grid.
                    </p>
                    <label>Teaching Assistant:</label>
                    <select id="select-ta">
                        ${options}
                    </select>
                    <div class="assign-legend flex">
                        <div id="legend-closed" class="legend-column">
                            <div class="legend-desc">Closed</div>
                            <div class="legend-item closed"></div>
                        </div>
                        <div class="legend-column">
                            <div id="legend-desc-busy" class="legend-desc">Busy</div>
                            <div class="legend-item busy"></div>
                        </div>
                        <div class="legend-column">
                            <div id="legend-desc-" class="legend-desc">N/A</div>
                            <div class="legend-item unavailable"></div>
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
            </div>
            <div id="right-grid-header">
                <div id="right-grid-header-content">
                    <h2>All Assignments</h2>
                    <p>
                        The grid below displays all current lab hour assignments
                        for the semester ${verboseSemester}. To modify an individual's
                        lab hour assignment, use the "Individual Assignments" grid.
                    </p>
                    <div class="view-assigned-legend flex">
                        <div id="legend-closed" class="legend-column">
                            <div class="legend-desc">Closed</div>
                            <div class="legend-item closed"></div>
                        </div>
                        <div class="legend-column">
                            <div id="legend-desc-free" class="legend-desc">Unassigned</div>
                            <div class="legend-item"></div>
                        </div>
                        ${taLegendColumns}
                    </div>
                </div>
            </div>
        </header>
        `;
    }

    function LabHourGrid(GridItems) {
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
                else if (!isAvailable)
                    className += ' busy';
                else if (isAssigned && !isSelected)
                    className += ' unavailable';
                else if (isOpen && isAvailable && isSelected)
                    className += ' selected';
                gridItems += AssignedGridItem({id, className});
            }
        }
        const gridStyle = utils.getLabHourGridStyle(numColumns, numRows);
        return `
        <div class="grid-container" style="${gridStyle}">
            ${gridItems}
        </div>
        `;
    }

    function AssignedGridItem({id, className}) {
        return `<div id="${id}" class="${className}"></div>`;

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
                const initials = getGridItemInitials(adjustedRow, col);
                let className = "read-only-grid-item";
                if (!isHour)
                    className += ' non-hour';
                if (!isOpen)
                    className += ' closed';
                if (isOpen && isAssigned) {
                    className += ' selected';
                    const style = `background-color: ${getGridItemColor(adjustedRow, col)};`
                    gridItems += ViewAssignedGridItem({id, className, style, initials});
                } else {
                    gridItems += ViewAssignedGridItem({id, className, initials});
                }
            }
        }
        const gridStyle = utils.getLabHourGridStyle(numColumns, numRows);
        return `
        <div class="read-only-grid-container" style="${gridStyle}">
            ${gridItems}
        </div>
        `;
    }

    function getGridItemInitials(row, col) {
        const eagleId = assignments[row][col];
        if (!eagleId) return '';
        const taName = tas[parseInt(eagleId)];
        const [first, last] = taName.split(' ');
        return `${first[0]}${last[0]}`
    }

    function getGridItemColor(row, col) {
        const assignedEagleId = assignments[row][col];
        const [r, g, b] = taColors[parseInt(assignedEagleId)];
        return `rgb(${r}, ${g}, ${b})`;
    }

    function ViewAssignedGridItem({id, className, style, initials}) {
        if (style) {
            return `
            <div id="${id}" class="${className}" style="${style}">
                <div class="read-only-grid-item-content">${initials}</div>
            </div>
            `;
        }
        return `
        <div id="${id}" class="${className}">
            <div class="read-only-grid-item-content">${initials}</div>
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

    function selectFromHere(e) {
        e.preventDefault();
        const {row, col} = utils.getRowAndCol(e.target.id);
        if (!isSelectable(row, col)) return;
        const isSelected = selected[row][col];
        shouldSelect = !isSelected;
        toggleSelection(row, col, !isSelected);
        fromCoordinates = {row, col};
        mouseDown = true;
    }

    function isSelectable(row, col) {
        const isOpen = constraints[row][col];
        const isAvailable = preferences[row][col];
        const isAssigned = !!assignments[row][col];
        const isAssignedToSelectedTA = assignments[row][col] == selectedEagleId;
        return isOpen 
            && isAvailable 
            && (!isAssigned || isAssignedToSelectedTA);
    }

    function toggleSelection(row, col, shouldSelectThisElement) {
        if (!isSelectable(row, col)) return;
        const element = utils.getElement(row, col);
        const isSelected = selected[row][col];
        selected[row][col] = shouldSelectThisElement;
        if (!isSelected && shouldSelectThisElement)
            element.className += ' selected';
        else if (isSelected && !shouldSelectThisElement)
            element.className = utils.rstrip(element.className, ' selected');
    }

    function selectToHere(e) {
        e.preventDefault();
        if (!mouseDown) return;
        let {row: rowTo, col: colTo} = toCoordinates;
        const isGridCell = e.target.className.includes('grid-item');
        if (isGridCell) toCoordinates = utils.getRowAndCol(e.target.id);
        toggleFromTo(toggleSelection);
        assignHours();
        mouseDown = false;
    }

    function assignHours() {
        selected.forEach((row, rowIdx) => {
            row.forEach((isSelected, colIdx) => {
                const isAssigned = assignments[rowIdx][colIdx] == selectedEagleId;
                if (isSelected)
                    assignments[rowIdx][colIdx] = selectedEagleId;
                else if (!isSelected && isAssigned)
                    assignments[rowIdx][colIdx] = '';
            })
        })
        render();
        setSelectedApplicant(selectedEagleId);
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
        e.preventDefault();
        if (!mouseDown) return;
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
                const isAssigned = assignments[row][col];
                if (isSelectable(row, col) && !isWithinFromToPlane(row, col)) {
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
        if (!isSelectable(row, col)) return;
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

    function highlightLegendItem(e, textColor, borderColor) {
        const {row, col} = utils.getRowAndCol(e.target.id);
        const eagleId = assignments[row][col];
        if (!eagleId) return;
        const legendDescription = document.querySelector(`#legend-desc-${eagleId}`);
        legendDescription.style.color = textColor;
        const legendItem = document.querySelector(`#legend-item-${eagleId}`);
        legendItem.style.borderColor = borderColor;
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

    async function changeTA(e) {
        selectedEagleId = e.target.value;
        preferences = await getPreferences(semester, selectedEagleId);
        selected = getAssignment(assignments, selectedEagleId);
        render();
        setSelectedApplicant(selectedEagleId);
    }

    function outputAssignments() {
        const labHourInput = document.querySelector('#id_lab_hour_data');
        labHourInput.value = JSON.stringify(assignments);
    }

    function render() {
        const labHourFormRoot = document.querySelector('#lab-hour-form');
        labHourFormRoot.innerHTML = LabHourAssignmentForm();
        const gridItems = document.querySelectorAll('.grid-item');
        gridItems.forEach(item => {
            item.onmousedown = selectFromHere;
            item.onmouseenter = highlightToHere;
            item.onmouseup = selectToHere;
        });
        const readOnlyGridItems = document.querySelectorAll('.read-only-grid-item');
        readOnlyGridItems.forEach(item => {
            item.onmouseenter = e => highlightLegendItem(e, '#c9ac16', '#c9ac16');
            item.onmouseleave = e => highlightLegendItem(e, 'black', 'var(--grid-color');
        });
        const selectTA = document.querySelector('#select-ta');
        selectTA.onchange = changeTA;
        const grid = document.querySelector('.grid-container');
        grid.oncontextmenu = e => e.preventDefault();
        window.onmouseup = selectToHere;
        window.onresize = resizeColHeaders;
        document.querySelector('#id_semester').value = semester;
        outputAssignments();
    }

    render();
}

renderLabHourAssignmentForm();
