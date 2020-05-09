import { renderLabHourForm } from '../ta_system/lab-hour-form.js';
import { initLabHourGrid, getLabHourData } from '../ta_system/lab-hour-utils.js';

const semester = document.querySelector('#lab-hour-semester').value;

renderLabHourForm({
    getConstraints: () => initLabHourGrid(true),
    getStartingGrid: () => getLabHourData({
        endpoint: `/admin/get_lab_hour_constraints?semester=${semester}`,
        defaultValue: false
    }),
    extraJS: () => {
        document.getElementById('legend-desc-busy').innerHTML = 'Closed';
        document.getElementById('legend-desc-free').innerHTML = 'Open';
        document.querySelector('#lab-hour-submit-button').value = 'Save Changes';
        document.querySelector('#id_semester').value = semester;
    }
});
