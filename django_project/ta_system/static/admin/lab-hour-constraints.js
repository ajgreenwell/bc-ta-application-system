import { renderLabHourForm } from '../ta_system/lab-hour-form.js';
import { initLabHourGrid } from '../ta_system/lab-hour-utils.js';

async function getStartingGrid() {
    const semester = document.querySelector('#lab-hour-semester').value;
    const res = await fetch(`/admin/get_lab_hour_constraints?semester=${semester}`);
    const data = await res.json();
    if (data && data.length) return data;
    return initLabHourGrid(false);
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
