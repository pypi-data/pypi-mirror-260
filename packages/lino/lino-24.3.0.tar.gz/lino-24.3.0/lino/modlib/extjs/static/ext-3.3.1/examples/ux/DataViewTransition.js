/*!
 * Ext JS Library 3.3.1
 * Copyright(c) 2006-2010 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
/**
 * @class Ext.ux.DataViewTransition
 * @extends Object
 * @author Ed Spencer (http://extjs.com)
 * Transition plugin for DataViews
 */
Ext.ux.DataViewTransition = Ext.extend(Object, {

    /**
     * @property defaults
     * @type Object
     * Default configuration options for all DataViewTransition instances
     */
    defaults: {
        duration  : 750,
        idProperty: 'id'
    },
    
    /**
     * Creates the plugin instance, applies defaults
     * @constructor
     * @param {Object} config Optional config object
     */
    constructor: function(config) {
        Ext.apply(this, config || {}, this.defaults);
    },

    /**
     * Initializes the transition plugin. Overrides the dataview's default refresh function
     * @param {Ext.DataView} dataview The dataview
     */
    init: function(dataview) {
        /**
         * @property dataview
         * @type Ext.DataView
         * Reference to the DataView this instance is bound to
         */
        this.dataview = dataview;
        
        var idProperty = this.idProperty;
        dataview.blockRefresh = true;
        dataview.updateIndexes = dataview.updateIndexes.createSequence(function() {
            this.getTemplateTarget().select(this.itemSelector).each(function(element, composite, index) {
                element.id = element.dom.id = String.format("{0}-{1}", dataview.id, store.getAt(index).get(idProperty));
            }, this);
        }, dataview);
        
        /**
         * @property dataviewID
         * @type String
         * The string ID of the DataView component. This is used internally when animating child objects
         */
        this.dataviewID = dataview.id;
        
        /**
         * @property cachedStoreData
         * @type Object
         * A cache of existing store data, keyed by id. This is used to determine
         * whether any items were added or removed from the store on data change
         */
        this.cachedStoreData = {};
        
        var store = dataview.store;
        
        //cache the data immediately, and again on any load operation
        this.cacheStoreData(store);
        store.on('load', this.cacheStoreData, this);
        
        store.on('datachanged', function(store) {
            var parentEl = dataview.getTemplateTarget(),
                calcItem = store.getAt(0),
                added    = this.getAdded(store),
                removed  = this.getRemoved(store),
                previous = this.getRemaining(store),
                existing = Ext.apply({}, previous, added);
            
            //hide old items
            Ext.each(removed, function(item) {
                Ext.fly(this.dataviewID + '-' + item.get(this.idProperty)).fadeOut({
                    remove  : false,
                    duration: duration / 1000,
                    useDisplay: true
                });
            }, this);
            
            //store is empty
            if (calcItem == undefined) {
                this.cacheStoreData(store);
                return;
            }
            
            var el = parentEl.child("#" + this.dataviewID + "-" + calcItem.get(this.idProperty));
            
            //calculate the number of rows and columns we have
            var itemCount   = store.getCount(),
                itemWidth   = el.getMargins('lr') + el.getWidth(),
                itemHeight  = el.getMargins('bt') + el.getHeight(),
                dvWidth     = parentEl.getWidth(),
                columns     = Math.floor(dvWidth / itemWidth),
                rows        = Math.ceil(itemCount / columns),
                currentRows = Math.ceil(this.getExistingCount() / columns);
            
            //make sure the correct styles are applied to the parent element
            parentEl.applyStyles({
                display : 'block',
                position: 'relative'
                // ,
                // height  : Ext.max([rows, currentRows]) * itemHeight,
                // width   : columns * itemWidth
            });
            
            //stores the current top and left values for each element (discovered below)
            var oldPositions = {},
                newPositions = {},
                elCache      = {};
            
            //find current positions of each element and save a reference in the elCache
            Ext.iterate(previous, function(id, item) {
                var id = item.get(this.idProperty),
                    el = elCache[id] = parentEl.child('#' + this.dataviewID + '-' + id);
                
                oldPositions[id] = {
                    top : el.getTop()  - parentEl.getTop()  - el.getMargins('t') - parentEl.getPadding('t'),
                    left: el.getLeft() - parentEl.getLeft() - el.getMargins('l') - parentEl.getPadding('l')
                };
            }, this);
            
            //set absolute positioning on all DataView items. We need to set position, left and 
            //top at the same time to avoid any flickering
            Ext.iterate(previous, function(id, item) {
                var oldPos = oldPositions[id],
                    el     = elCache[id];
                    
                if (el.getStyle('position') != 'absolute') {
                    elCache[id].applyStyles({
                        position: 'absolute',
                        left    : oldPos.left + "px",
                        top     : oldPos.top + "px",

                        //we set the width here to make ListViews work correctly. This is not needed for DataViews
                        width   : el.getWidth(!Ext.isIE || Ext.isStrict),
                        height  : el.getHeight(!Ext.isIE || Ext.isStrict)
                    });
                }
            });
            
            //get new positions
            var index = 0;
            Ext.iterate(store.data.items, function(item) {
                var id = item.get(idProperty),
                    el = elCache[id];
                
                var column = index % columns,
                    row    = Math.floor(index / columns),
                    top    = row    * itemHeight,
                    left   = column * itemWidth;
                
                newPositions[id] = {
                    top : top,
                    left: left
                };
                
                index ++;
            }, this);
            
            //do the movements
            var startTime  = new Date(),
                duration   = this.duration,
                dataviewID = this.dataviewID;
            
            var doAnimate = function() {
                var elapsed  = new Date() - startTime,
                    fraction = elapsed / duration;
                
                if (fraction >= 1) {
                    for (var id in newPositions) {
                        Ext.fly(dataviewID + '-' + id).applyStyles({
                            top : newPositions[id].top + "px",
                            left: newPositions[id].left + "px"
                        });
                    }
                    
                    Ext.TaskMgr.stop(task);
                } else {
                    //move each item
                    for (var id in newPositions) {
                        if (!previous[id]) continue;
                        
                        var oldPos  = oldPositions[id],
                            newPos  = newPositions[id],
                            oldTop  = oldPos.top,
                            newTop  = newPos.top,
                            oldLeft = oldPos.left,
                            newLeft = newPos.left,
                            diffTop = fraction * Math.abs(oldTop  - newTop),
                            diffLeft= fraction * Math.abs(oldLeft - newLeft),
                            midTop  = oldTop  > newTop  ? oldTop  - diffTop  : oldTop  + diffTop,
                            midLeft = oldLeft > newLeft ? oldLeft - diffLeft : oldLeft + diffLeft;
                        
                        Ext.fly(dataviewID + '-' + id).applyStyles({
                            top : midTop + "px",
                            left: midLeft + "px"
                        });
                    }
                }
            };
            
            var task = {
                run     : doAnimate,
                interval: 20,
                scope   : this
            };
            
            Ext.TaskMgr.start(task);
            
            //show new items
            Ext.iterate(added, function(id, item) {
                Ext.fly(this.dataviewID + '-' + item.get(this.idProperty)).applyStyles({
                    top : newPositions[id].top + "px",
                    left: newPositions[id].left + "px"
                }).fadeIn({
                    remove  : false,
                    duration: duration / 1000
                });
            }, this);
            
            this.cacheStoreData(store);
        }, this);
    },
    
    /**
     * Caches the records from a store locally for comparison later
     * @param {Ext.data.Store} store The store to cache data from
     */
    cacheStoreData: function(store) {
        this.cachedStoreData = {};
        
        store.each(function(record) {
             this.cachedStoreData[record.get(this.idProperty)] = record;
        }, this);
    },
    
    /**
     * Returns all records that were already in the DataView
     * @return {Object} All existing records
     */
    getExisting: function() {
        return this.cachedStoreData;
    },
    
    /**
     * Returns the total number of items that are currently visible in the DataView
     * @return {Number} The number of existing items
     */
    getExistingCount: function() {
        var count = 0,
            items = this.getExisting();
        
        for (var k in items) count++;
        
        return count;
    },
    
    /**
     * Returns all records in the given store that were not already present
     * @param {Ext.data.Store} store The updated store instance
     * @return {Object} Object of records not already present in the dataview in format {id: record}
     */
    getAdded: function(store) {
        var added = {};
        
        store.each(function(record) {
            if (this.cachedStoreData[record.get(this.idProperty)] == undefined) {
                added[record.get(this.idProperty)] = record;
            }
        }, this);
        
        return added;
    },
    
    /**
     * Returns all records that are present in the DataView but not the new store
     * @param {Ext.data.Store} store The updated store instance
     * @return {Array} Array of records that used to be present
     */
    getRemoved: function(store) {
        var removed = [];
        
        for (var id in this.cachedStoreData) {
            if (store.findExact(this.idProperty, Number(id)) == -1) removed.push(this.cachedStoreData[id]);
        }
        
        return removed;
    },
    
    /**
     * Returns all records that are already present and are still present in the new store
     * @param {Ext.data.Store} store The updated store instance
     * @return {Object} Object of records that are still present from last time in format {id: record}
     */
    getRemaining: function(store) {
      var remaining = {};
      
      store.each(function(record) {
          if (this.cachedStoreData[record.get(this.idProperty)] != undefined) {
              remaining[record.get(this.idProperty)] = record;
          }
      }, this);
      
      return remaining;
    }
});