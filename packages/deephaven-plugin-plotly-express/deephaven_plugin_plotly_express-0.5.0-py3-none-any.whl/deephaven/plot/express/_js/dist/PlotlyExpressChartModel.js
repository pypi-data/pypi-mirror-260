import { ChartModel, ChartUtils } from '@deephaven/chart';
import Log from '@deephaven/log';
import { getDataMappings, getWidgetData, removeColorsFromData, } from './PlotlyExpressChartUtils.js';
const log = Log.module('@deephaven/js-plugin-plotly-express.ChartModel');
export class PlotlyExpressChartModel extends ChartModel {
    constructor(dh, widget, refetch) {
        super(dh);
        this.isSubscribed = false;
        /**
         * Map of table index to Table object.
         */
        this.tableReferenceMap = new Map();
        /**
         * Map of table index to TableSubscription object.
         */
        this.tableSubscriptionMap = new Map();
        /**
         * Map of table index to cleanup function for the subscription.
         */
        this.subscriptionCleanupMap = new Map();
        /**
         * Map of table index to map of column names to array of paths where the data should be replaced.
         */
        this.tableColumnReplacementMap = new Map();
        /**
         * Map of table index to ChartData object. Used to handle data delta updates.
         */
        this.chartDataMap = new Map();
        /**
         * Map of table index to object where the keys are column names and the values are arrays of data.
         * This data is the full array of data for the column since ChartData doesn't have a clean way to get it at any time.
         */
        this.tableDataMap = new Map();
        this.plotlyData = [];
        this.layout = {};
        this.isPaused = false;
        this.hasPendingUpdate = false;
        this.hasInitialLoadCompleted = false;
        this.widget = widget;
        this.refetch = refetch;
        this.chartUtils = new ChartUtils(dh);
        this.handleFigureUpdated = this.handleFigureUpdated.bind(this);
        this.handleWidgetUpdated = this.handleWidgetUpdated.bind(this);
        // This is mostly used for setting the initial layout.
        // Chart only fetches the model layout once on init, so it needs to be set
        // before the widget is subscribed to.
        this.handleWidgetUpdated(getWidgetData(widget), widget.exportedObjects);
        this.setTitle(this.getDefaultTitle());
    }
    getData() {
        const hydratedData = [...this.plotlyData];
        this.tableColumnReplacementMap.forEach((columnReplacements, tableId) => {
            const tableData = this.tableDataMap.get(tableId);
            if (tableData == null) {
                throw new Error(`No tableData for table ID ${tableId}`);
            }
            // Replace placeholder arrays with actual data
            columnReplacements.forEach((paths, columnName) => {
                paths.forEach(destination => {
                    var _a;
                    // The JSON pointer starts w/ /plotly/data and we don't need that part
                    const parts = destination
                        .split('/')
                        .filter(part => part !== '' && part !== 'plotly' && part !== 'data');
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    let selector = hydratedData;
                    for (let i = 0; i < parts.length; i += 1) {
                        if (i !== parts.length - 1) {
                            selector = selector[parts[i]];
                        }
                        else {
                            selector[parts[i]] = (_a = tableData[columnName]) !== null && _a !== void 0 ? _a : [];
                        }
                    }
                });
            });
        });
        return hydratedData;
    }
    getLayout() {
        return this.layout;
    }
    close() {
        var _a;
        super.close();
        (_a = this.widget) === null || _a === void 0 ? void 0 : _a.close();
        this.widget = undefined;
    }
    async subscribe(callback) {
        if (this.isSubscribed) {
            return;
        }
        super.subscribe(callback);
        if (this.widget == null) {
            this.widget = await this.refetch();
            const widgetData = getWidgetData(this.widget);
            this.handleWidgetUpdated(widgetData, this.widget.exportedObjects);
        }
        this.isSubscribed = true;
        this.widgetUnsubscribe = this.widget.addEventListener(this.dh.Widget.EVENT_MESSAGE, ({ detail }) => {
            this.handleWidgetUpdated(JSON.parse(detail.getDataAsString()), detail.exportedObjects);
        });
        this.tableReferenceMap.forEach((_, id) => this.subscribeTable(id));
        // If there are no tables to fetch data from, the chart is ready to render
        // Normally this event only fires once at least 1 table has fetched data
        // Without this, the chart shows an infinite loader if there are no tables
        if (this.tableColumnReplacementMap.size === 0) {
            this.fireUpdate(this.getData());
        }
    }
    unsubscribe(callback) {
        var _a, _b;
        if (!this.isSubscribed) {
            return;
        }
        super.unsubscribe(callback);
        (_a = this.widgetUnsubscribe) === null || _a === void 0 ? void 0 : _a.call(this);
        this.isSubscribed = false;
        this.tableReferenceMap.forEach((_, id) => this.removeTable(id));
        (_b = this.widget) === null || _b === void 0 ? void 0 : _b.close();
        this.widget = undefined;
    }
    updateLayout(data) {
        const { figure } = data;
        const { plotly } = figure;
        const { layout: plotlyLayout = {} } = plotly;
        this.layout = Object.assign({}, plotlyLayout);
    }
    handleWidgetUpdated(data, references) {
        var _a, _b, _c;
        const { figure, new_references: newReferences, removed_references: removedReferences, } = data;
        const { plotly, deephaven } = figure;
        const { layout: plotlyLayout = {} } = plotly;
        this.tableColumnReplacementMap = getDataMappings(data);
        this.plotlyData = plotly.data;
        this.updateLayout(data);
        if (!deephaven.is_user_set_template) {
            removeColorsFromData((_c = (_b = (_a = plotlyLayout === null || plotlyLayout === void 0 ? void 0 : plotlyLayout.template) === null || _a === void 0 ? void 0 : _a.layout) === null || _b === void 0 ? void 0 : _b.colorway) !== null && _c !== void 0 ? _c : [], this.plotlyData);
        }
        newReferences.forEach(async (id, i) => {
            this.tableDataMap.set(id, {}); // Plot may render while tables are being fetched. Set this to avoid a render error
            const table = (await references[i].fetch());
            this.addTable(id, table);
        });
        removedReferences.forEach(id => this.removeTable(id));
    }
    handleFigureUpdated(event, tableId) {
        const chartData = this.chartDataMap.get(tableId);
        const tableData = this.tableDataMap.get(tableId);
        if (chartData == null) {
            log.warn('Unknown chartData for this event. Skipping update');
            return;
        }
        if (tableData == null) {
            log.warn('No tableData for this event. Skipping update');
            return;
        }
        const { detail: figureUpdateEvent } = event;
        chartData.update(figureUpdateEvent);
        figureUpdateEvent.columns.forEach(column => {
            const columnData = chartData.getColumn(column.name, this.chartUtils.unwrapValue, figureUpdateEvent);
            tableData[column.name] = columnData;
        });
        if (this.isPaused) {
            this.hasPendingUpdate = true;
            return;
        }
        this.fireUpdate(this.getData());
    }
    addTable(id, table) {
        if (this.tableReferenceMap.has(id)) {
            return;
        }
        this.tableReferenceMap.set(id, table);
        this.tableDataMap.set(id, {});
        if (this.isSubscribed) {
            this.subscribeTable(id);
        }
    }
    subscribeTable(id) {
        const table = this.tableReferenceMap.get(id);
        const columnReplacements = this.tableColumnReplacementMap.get(id);
        if (table != null &&
            columnReplacements != null &&
            columnReplacements.size > 0 &&
            !this.tableSubscriptionMap.has(id)) {
            this.chartDataMap.set(id, new this.dh.plot.ChartData(table));
            const columnNames = new Set(columnReplacements.keys());
            const columns = table.columns.filter(({ name }) => columnNames.has(name));
            const subscription = table.subscribe(columns);
            this.tableSubscriptionMap.set(id, subscription);
            this.subscriptionCleanupMap.set(id, subscription.addEventListener(this.dh.Table.EVENT_UPDATED, e => this.handleFigureUpdated(e, id)));
        }
    }
    removeTable(id) {
        var _a, _b;
        (_a = this.subscriptionCleanupMap.get(id)) === null || _a === void 0 ? void 0 : _a();
        (_b = this.tableSubscriptionMap.get(id)) === null || _b === void 0 ? void 0 : _b.close();
        this.tableReferenceMap.delete(id);
        this.subscriptionCleanupMap.delete(id);
        this.tableSubscriptionMap.delete(id);
        this.chartDataMap.delete(id);
        this.tableDataMap.delete(id);
        this.tableColumnReplacementMap.delete(id);
    }
    fireUpdate(data) {
        super.fireUpdate(data);
        this.hasPendingUpdate = false;
        // TODO: This will fire on first call to `fireUpdate` even though other data
        // may still be loading. We should consider making this smarter to fire after
        // all initial data has loaded.
        // https://github.com/deephaven/deephaven-plugins/issues/267
        if (!this.hasInitialLoadCompleted) {
            this.fireLoadFinished();
            this.hasInitialLoadCompleted = true;
        }
    }
    pauseUpdates() {
        this.isPaused = true;
    }
    resumeUpdates() {
        this.isPaused = false;
        if (this.hasPendingUpdate) {
            this.fireUpdate(this.getData());
        }
    }
    shouldPauseOnUserInteraction() {
        return (this.hasScene() || this.hasGeo() || this.hasMapbox() || this.hasPolar());
    }
    hasScene() {
        return this.plotlyData.some(d => 'scene' in d && d.scene != null);
    }
    hasGeo() {
        return this.plotlyData.some(d => 'geo' in d && d.geo != null);
    }
    hasMapbox() {
        return this.plotlyData.some(({ type }) => type === null || type === void 0 ? void 0 : type.includes('mapbox'));
    }
    hasPolar() {
        return this.plotlyData.some(({ type }) => type === null || type === void 0 ? void 0 : type.includes('polar'));
    }
    getPlotWidth() {
        var _a, _b, _c, _d;
        if (!this.rect || !this.rect.width) {
            return 0;
        }
        return Math.max(this.rect.width -
            ((_b = (_a = this.layout.margin) === null || _a === void 0 ? void 0 : _a.l) !== null && _b !== void 0 ? _b : 0) -
            ((_d = (_c = this.layout.margin) === null || _c === void 0 ? void 0 : _c.r) !== null && _d !== void 0 ? _d : 0), 0);
    }
    getPlotHeight() {
        var _a, _b, _c, _d;
        if (!this.rect || !this.rect.height) {
            return 0;
        }
        return Math.max(this.rect.height -
            ((_b = (_a = this.layout.margin) === null || _a === void 0 ? void 0 : _a.t) !== null && _b !== void 0 ? _b : 0) -
            ((_d = (_c = this.layout.margin) === null || _c === void 0 ? void 0 : _c.b) !== null && _d !== void 0 ? _d : 0), 0);
    }
}
export default PlotlyExpressChartModel;
//# sourceMappingURL=PlotlyExpressChartModel.js.map