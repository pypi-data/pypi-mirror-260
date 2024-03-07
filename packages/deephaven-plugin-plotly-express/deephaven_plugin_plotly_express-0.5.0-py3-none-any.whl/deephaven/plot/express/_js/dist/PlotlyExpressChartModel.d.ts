import type { Layout, Data } from 'plotly.js';
import type { dh as DhType, ChartData, Widget, Table, TableSubscription, TableData } from '@deephaven/jsapi-types';
import { ChartModel, ChartUtils } from '@deephaven/chart';
import { PlotlyChartWidgetData } from './PlotlyExpressChartUtils.js';
export declare class PlotlyExpressChartModel extends ChartModel {
    constructor(dh: DhType, widget: Widget, refetch: () => Promise<Widget>);
    isSubscribed: boolean;
    chartUtils: ChartUtils;
    refetch: () => Promise<Widget>;
    widget?: Widget;
    widgetUnsubscribe?: () => void;
    /**
     * Map of table index to Table object.
     */
    tableReferenceMap: Map<number, Table>;
    /**
     * Map of table index to TableSubscription object.
     */
    tableSubscriptionMap: Map<number, TableSubscription>;
    /**
     * Map of table index to cleanup function for the subscription.
     */
    subscriptionCleanupMap: Map<number, () => void>;
    /**
     * Map of table index to map of column names to array of paths where the data should be replaced.
     */
    tableColumnReplacementMap: Map<number, Map<string, string[]>>;
    /**
     * Map of table index to ChartData object. Used to handle data delta updates.
     */
    chartDataMap: Map<number, ChartData>;
    /**
     * Map of table index to object where the keys are column names and the values are arrays of data.
     * This data is the full array of data for the column since ChartData doesn't have a clean way to get it at any time.
     */
    tableDataMap: Map<number, {
        [key: string]: unknown[];
    }>;
    plotlyData: Data[];
    layout: Partial<Layout>;
    isPaused: boolean;
    hasPendingUpdate: boolean;
    hasInitialLoadCompleted: boolean;
    getData(): Partial<Data>[];
    getLayout(): Partial<Layout>;
    close(): void;
    subscribe(callback: (event: CustomEvent) => void): Promise<void>;
    unsubscribe(callback: (event: CustomEvent) => void): void;
    updateLayout(data: PlotlyChartWidgetData): void;
    handleWidgetUpdated(data: PlotlyChartWidgetData, references: Widget['exportedObjects']): void;
    handleFigureUpdated(event: CustomEvent<TableData>, tableId: number): void;
    addTable(id: number, table: Table): void;
    subscribeTable(id: number): void;
    removeTable(id: number): void;
    fireUpdate(data: unknown): void;
    pauseUpdates(): void;
    resumeUpdates(): void;
    shouldPauseOnUserInteraction(): boolean;
    hasScene(): boolean;
    hasGeo(): boolean;
    hasMapbox(): boolean;
    hasPolar(): boolean;
    getPlotWidth(): number;
    getPlotHeight(): number;
}
export default PlotlyExpressChartModel;
//# sourceMappingURL=PlotlyExpressChartModel.d.ts.map