import { renderLabHourForm } from '../ta_system/lab-hour-form.js';
import { initLabHourGrid, getLabHourConstraints } from '../ta_system/lab-hour-utils.js';

async function getStartingGrid() {
    const semester = document.querySelector('#lab-hour-semester').value;
    const endpoint = `/admin/get_lab_hour_constraints?semester=${semester}`;
    getLabHourConstraints(endpoint, false);
}

function moodifyForConstraintsForm() {
    document.getElementById('legend-desc-busy').innerHTML = 'Closed';
    document.getElementById('legend-desc-free').innerHTML = 'Open';
    document.querySelector('#lab-hour-submit-button').value = 'Save Changes';
    const semester = document.querySelector('#lab-hour-semester').value;
    document.querySelector('#id_semester').value = semester;
}

renderLabHourForm({
    getConstraints: () => initLabHourGrid(true),
    getStartingGrid: getStartingGrid,
    extraJS: moodifyForConstraintsForm
});
