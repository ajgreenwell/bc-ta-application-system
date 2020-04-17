import { renderLabHourForm } from './lab-hour-form.js';
import { getLabHourConstraints, getLabHourPreferences } from './lab-hour-utils.js';

function getConstraints() {
    const endpoint = '/get_lab_hour_constraints/';
    return getLabHourConstraints(endpoint, true);
}

function changeSubmitButtonText() {
    document.querySelector('#lab-hour-submit-button').value = 'Save Changes';
}

renderLabHourForm({
    getConstraints: getConstraints,
    getStartingGrid: getLabHourPreferences,
    extraJS: changeSubmitButtonText
});
