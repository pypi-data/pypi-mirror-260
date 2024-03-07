import type { Data, PlotlyDataLayoutConfig } from 'plotly.js';
import type { Table, Widget } from '@deephaven/jsapi-types';
export interface PlotlyChartWidget {
    getDataAsBase64(): string;
    exportedObjects: {
        fetch(): Promise<Table>;
    }[];
    addEventListener(type: string, fn: (event: CustomEvent<PlotlyChartWidget>) => () => void): void;
}
export interface PlotlyChartWidgetData {
    type: string;
    figure: {
        deephaven: {
            mappings: Array<{
                table: number;
                data_columns: Record<string, string[]>;
            }>;
            is_user_set_template: boolean;
            is_user_set_color: boolean;
        };
        plotly: PlotlyDataLayoutConfig;
    };
    revision: number;
    new_references: number[];
    removed_references: number[];
}
export declare function getWidgetData(widgetInfo: Widget): PlotlyChartWidgetData;
export declare function getDataMappings(widgetData: PlotlyChartWidgetData): Map<number, Map<string, string[]>>;
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
export declare function removeColorsFromData(colorway: string[], data: Data[]): void;
//# sourceMappingURL=PlotlyExpressChartUtils.d.ts.map