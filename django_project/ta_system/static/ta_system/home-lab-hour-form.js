import { renderLabHourForm } from './lab-hour-form.js';
import { getLabHourData } from './lab-hour-utils.js';

renderLabHourForm({
    getConstraints: () => getLabHourData({
        endpoint: '/get_lab_hour_constraints/',
        defaultValue: true
    }),
    getStartingGrid: () => getLabHourData({
        endpoint: '/get_lab_hour_preferences/',
        defaultValue: false
    }),
    extraJS: null
});
