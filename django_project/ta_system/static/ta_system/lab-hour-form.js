import * as utils from './lab-hour-utils.js';
import * as settings from './lab-hour-settings.js';
import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@rc/dist/js.cookie.min.mjs';


export async function renderLabHourForm({ redirect }) {
    const constraints = utils.getLabHourConstraints();
    const [startHour, endHour] = utils.getStartAndEndHour(constraints);
    let labHourPreferences = await utils.getLabHourPreferences();
    let mouseDown = false;

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
                const isSelected = labHourPreferences[adjustedRow][col];
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
                <div class="legend-column">
                    <div class="legend-desc">N/A</div>
                    <div class="legend-item closed"></div>
                </div>
                <div class="legend-column">
                    <div class="legend-desc">Busy</div>
                    <div class="legend-item"></div>
                </div>
                <div class="legend-column">
                    <div class="legend-desc">Free</div>
                    <div class="legend-item selected"></div>
                </div>
            </div>
        `;
    }

    function selectFromHere(e) {
        mouseDown = true;
        const className = e.target.className;
        const [row, col] = utils.getRowAndCol(e.target.id);
        const isClosed = !constraints[row][col];
        const isSelected = className.includes('selected');
        if (isClosed)
            return;
        if (isSelected) {
            e.target.className = utils.rstrip(className, ' selected');
            labHourPreferences[row][col] = false;

        } else {
            e.target.className += ' selected';
            labHourPreferences[row][col] = true;
        }
        outputLabHourPreferences()
    }

    function selectToHere(e) {
        if (mouseDown) selectFromHere(e);
    }

    function stopSelecting(e) {
        mouseDown = false;
    }

    function resizeColHeaders(e) {
        const colHeaders = document.querySelector('.col-headers');
        const numLetters = utils.getNumColHeaderLetters(e.target);
        colHeaders.innerHTML = ColumnHeaders(settings.daysOpen, numLetters);
    }

    function outputLabHourPreferences() {
        const labHourInput = document.querySelector('#id_lab_hour_preferences');
        labHourInput.value = JSON.stringify(labHourPreferences);
    }

    const labHourFormRoot = document.querySelector('#lab-hour-form');
    if (!labHourFormRoot) return;
    labHourFormRoot.innerHTML = LabHourGrid();
    const timeSlots = document.querySelectorAll('.grid-item');
    timeSlots.forEach(slot => {
        slot.onmousedown = selectFromHere;
        slot.onmouseover = selectToHere;
    });
    window.onmouseup = stopSelecting;
    window.onresize = resizeColHeaders;
    outputLabHourPreferences();
}
