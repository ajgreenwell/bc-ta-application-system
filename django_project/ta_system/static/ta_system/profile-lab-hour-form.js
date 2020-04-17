import { renderLabHourForm } from './lab-hour-form.js';
import { getLabHourConstraints, getLabHourPreferences } from './lab-hour-utils.js';

function changeSubmitButtonText() {
    document.querySelector('#lab-hour-submit-button').value = 'Save Changes';
}

renderLabHourForm({
    getConstraints: () => getLabHourConstraints(true),
    getStartingGrid: getLabHourPreferences,
    extraJS: changeSubmitButtonText
});
