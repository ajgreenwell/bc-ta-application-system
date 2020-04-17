import { renderLabHourForm } from './lab-hour-form.js';
import { getLabHourConstraints, getLabHourPreferences } from './lab-hour-utils.js';

renderLabHourForm({
    getConstraints: () => getLabHourConstraints(true),
    getStartingGrid: getLabHourPreferences,
    extraJS: null
});
