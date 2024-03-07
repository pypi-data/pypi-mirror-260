export function getWidgetData(widgetInfo) {
    return JSON.parse(widgetInfo.getDataAsString());
}
export function getDataMappings(widgetData) {
    const data = widgetData.figure;
    // Maps a reference index to a map of column name to an array of the paths where its data should be
    const tableColumnReplacementMap = new Map();
    data.deephaven.mappings.forEach(({ table: tableIndex, data_columns: dataColumns }) => {
        var _a;
        const existingColumnMap = (_a = tableColumnReplacementMap.get(tableIndex)) !== null && _a !== void 0 ? _a : new Map();
        tableColumnReplacementMap.set(tableIndex, existingColumnMap);
        // For each { columnName: [replacePaths] } in the object, add to the tableColumnReplacementMap
        Object.entries(dataColumns).forEach(([columnName, paths]) => {
            const existingPaths = existingColumnMap.get(columnName);
            if (existingPaths !== undefined) {
                existingPaths.push(...paths);
            }
            else {
                existingColumnMap.set(columnName, [...paths]);
            }
        });
    });
    return tableColumnReplacementMap;
}
/**
 * Removes the default colors from the data
 * Data color is not removed if the user set the color specifically or the plot type sets it
 *
 * This only checks if the marker or line color is set to a color in the colorway.
 * This means it is not possible to change the order of the colorway and use the same colors.
 *
 * @param colorway The colorway from plotly
 * @param data The data to remove the colorway from. This will be mutated
 */
export function removeColorsFromData(colorway, data) {
    const plotlyColors = new Set(colorway.map(color => color.toUpperCase()));
    // Just check if the colors are in the colorway at any point
    // Plotly has many different ways to layer/order series
    for (let i = 0; i < data.length; i += 1) {
        const trace = data[i];
        // There are multiple datatypes in plotly and some don't contain marker or marker.color
        if ('marker' in trace &&
            trace.marker != null &&
            'color' in trace.marker &&
            typeof trace.marker.color === 'string') {
            if (plotlyColors.has(trace.marker.color.toUpperCase())) {
                delete trace.marker.color;
            }
        }
        if ('line' in trace &&
            trace.line != null &&
            'color' in trace.line &&
            typeof trace.line.color === 'string') {
            if (plotlyColors.has(trace.line.color.toUpperCase())) {
                delete trace.line.color;
            }
        }
    }
}
//# sourceMappingURL=PlotlyExpressChartUtils.js.map