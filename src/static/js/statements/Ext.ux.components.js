Ext.ux.msg = function () {
    var msgCt;

    function createBox(title, text, type) {
        return ['<div class="msg">',
            '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
            '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc">',
            '<div class="ext-mb-icon ', type , '">',
            '<h3>', title, '</h3>', text,
            '</div></div></div></div>',
            '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
            '</div>'].join('');
    }

    return function (title, text, type, callback) {
        var delay = 1;
        if (type == "ext-mb-error") {
            delay = 10;
        } else if (type == "ext-mb-invisible") {
            delay = 1;
        } else {
            delay = 3;
        }
        if (!msgCt) {
            msgCt = Ext.DomHelper.insertFirst(document.body, {id: 'msg-div'}, true)
        }
        msgCt.alignTo(document, 't-t');
        var m = Ext.DomHelper.append(msgCt, {html: createBox(title, text, type)}, true);
        if (Ext.isFunction(callback)) {
            m.slideIn('t').pause(delay).ghost("t", {remove: true, callback: callback});
        } else {
            m.slideIn('t').pause(delay).ghost("t", {remove: true});
        }
    }
}();

Ext.ux.traceback = function () {

    function createBox(text, token) {

        return [
            '<form action="/traceback/" id="traceback-form" method="POST">',
            '<input type="hidden" name="csrfmiddlewaretoken" value="' + token + '" />',
            '<label for="traceback-content">трейсбек:</label>',
            '<br />',
            '<textarea id="traceback-content" cols="75" rows="8" name=traceback disabled>',
            text,
            '</textarea>',
            '<br />',
            '<label for="traceback-description">',
            'опишите Ваши действия перед сбоем <br />',
            'это поможет решить проблему быстрее <br />',
            '</label>',
            '<textarea id="traceback-descripton" cols="75" rows="10" name=traceback-descr>',
            '</textarea>',
            '<br />',
            '</form>'
        ].join('')
    }

    return function (title, text, token) {

        new Ext.Window({
            title: title,
            plain: true,
            html: createBox(text, token),
            modal: true,
            width: 600,
            buttons: [
                {
                    text: 'отослать отчёт',
                    handler: function () {
                        $("#traceback-content").removeAttr("disabled");
                        Ext.get("traceback-form").dom.submit();
                    }
                }
            ]
        }).show();
    }

}();

Ext.ux.mnuContext = new Ext.menu.Menu({
    items: [{
        id: 'split',
        text: 'Розділити'
    }],
    data: {},
    listeners: {
        itemclick: function(item) {
            switch (item.id) {
                case 'split':
                    window.split_popup = new Ext.ux.PopupWindow();
                    split_popup.title='Розділити позицію №' + this.data.id || '[id]';
                    split_popup.data = this.data;
                    split_popup.items.add(
                        new Ext.ux.SplitPanel({
                            data: this.data
                        })
                    );
                    split_popup.show();
                    break;
            }
        }
    }
});

Ext.ux.PopupWindow = Ext.extend(Ext.Window,{
    initComponent: function(){
        var config = {
            title: 'popup title',
            layout: 'fit',
            height: 180,
            width: 360,
            closable: true,
            resizable: false,
            draggable: true,
            items: []
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.PopupWindow.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.SplitPanel = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            padding: 10,
            items: [
                new Ext.form.Label({
                    html: this.data.data.descr
                }),
                new Ext.form.Label({
                    html: "<br /> " + this.data.data.amount + " грн."
                }),
                this.slider = new Ext.Slider({
                    value: 0,
                    increment: 0.01,
                    minValue: 0.01,
                    maxValue: this.data.data.amount-0.01,
                    listeners: {
                        change: {
                            fn: function ( slider, newValue, thumb ) {
                                this.field.setValue(newValue)
                            },
                            scope: this
                        }
                    }
                }),
                this.field = new Ext.form.NumberField({
                    value: 1,
                    minValue: 0.01,
                    maxValue: this.data.data.amount-0.01,
                    enableKeyEvents: true,
                    tm: 0,
                    listeners: {
                        keypress: {
                            fn: function (el, e) {
                                var $this = this;
                                if($this.field.validate()) {
                                    if($this.tm) {
                                        clearTimeout($this.tm)
                                    }
                                    this.tm = setTimeout(function(){
                                        $this.slider.setValue($this.field.getRawValue());
                                    }, 300);
                                }
                            },
                            scope: this
                        }
                    }
                }),
                new Ext.Button({
                    text: 'розділити',
                    handler: function() {
                        var $this = this;
                        MainApi.split_entry($this.data.id, $this.field.getValue(), function(response){
                            if(response.success) {
                                $this.data.store.reload();
                                window.split_popup.close();
                            }
                        })
                    },
                    scope: this
                })
            ],
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.SplitPanel.superclass.initComponent.apply(this, arguments);
    }
});

/*!
 * Ext JS Library 3.4.0
 * Copyright(c) 2006-2011 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
Ext.ns('Ext.ux.grid');

/**
 * @class Ext.ux.grid.BufferView
 * @extends Ext.grid.GridView
 * A custom GridView which renders rows on an as-needed basis.
 */
Ext.ux.grid.BufferView = Ext.extend(Ext.grid.GridView, {
    /**
     * @cfg {Number} rowHeight
     * The height of a row in the grid.
     */
    rowHeight: 19,

    /**
     * @cfg {Number} borderHeight
     * The combined height of border-top and border-bottom of a row.
     */
    borderHeight: 2,

    /**
     * @cfg {Boolean/Number} scrollDelay
     * The number of milliseconds before rendering rows out of the visible
     * viewing area. Defaults to 100. Rows will render immediately with a config
     * of false.
     */
    scrollDelay: 100,

    /**
     * @cfg {Number} cacheSize
     * The number of rows to look forward and backwards from the currently viewable
     * area.  The cache applies only to rows that have been rendered already.
     */
    cacheSize: 20,

    /**
     * @cfg {Number} cleanDelay
     * The number of milliseconds to buffer cleaning of extra rows not in the
     * cache.
     */
    cleanDelay: 500,

    initTemplates: function () {
        Ext.ux.grid.BufferView.superclass.initTemplates.call(this);
        var ts = this.templates;
        // empty div to act as a place holder for a row
        ts.rowHolder = new Ext.Template(
            '<div class="x-grid3-row {alt}" style="{tstyle}"></div>'
        );
        ts.rowHolder.disableFormats = true;
        ts.rowHolder.compile();

        ts.rowBody = new Ext.Template(
            '<table class="x-grid3-row-table" border="0" cellspacing="0" cellpadding="0" style="{tstyle}">',
            '<tbody><tr>{cells}</tr>',
            (this.enableRowBody ? '<tr class="x-grid3-row-body-tr" style="{bodyStyle}"><td colspan="{cols}" class="x-grid3-body-cell" tabIndex="0" hidefocus="on"><div class="x-grid3-row-body">{body}</div></td></tr>' : ''),
            '</tbody></table>'
        );
        ts.rowBody.disableFormats = true;
        ts.rowBody.compile();
    },

    getStyleRowHeight: function () {
        return Ext.isBorderBox ? (this.rowHeight + this.borderHeight) : this.rowHeight;
    },

    getCalculatedRowHeight: function () {
        return this.rowHeight + this.borderHeight;
    },

    getVisibleRowCount: function () {
        var rh = this.getCalculatedRowHeight(),
            visibleHeight = this.scroller.dom.clientHeight;
        return (visibleHeight < 1) ? 0 : Math.ceil(visibleHeight / rh);
    },

    getVisibleRows: function () {
        var count = this.getVisibleRowCount(),
            sc = this.scroller.dom.scrollTop,
            start = (sc === 0 ? 0 : Math.floor(sc / this.getCalculatedRowHeight()) - 1);
        return {
            first: Math.max(start, 0),
            last: Math.min(start + count + 2, this.ds.getCount() - 1)
        };
    },

    doRender: function (cs, rs, ds, startRow, colCount, stripe, onlyBody) {
        var ts = this.templates,
            ct = ts.cell,
            rt = ts.row,
            rb = ts.rowBody,
            last = colCount - 1,
            rh = this.getStyleRowHeight(),
            vr = this.getVisibleRows(),
            tstyle = 'width:' + this.getTotalWidth() + ';height:' + rh + 'px;',
        // buffers
            buf = [],
            cb,
            c,
            p = {},
            rp = {tstyle: tstyle},
            r;
        for (var j = 0, len = rs.length; j < len; j++) {
            r = rs[j];
            cb = [];
            var rowIndex = (j + startRow),
                visible = rowIndex >= vr.first && rowIndex <= vr.last;
            if (visible) {
                for (var i = 0; i < colCount; i++) {
                    c = cs[i];
                    p.id = c.id;
                    p.css = i === 0 ? 'x-grid3-cell-first ' : (i == last ? 'x-grid3-cell-last ' : '');
                    p.attr = p.cellAttr = "";
                    p.value = c.renderer(r.data[c.name], p, r, rowIndex, i, ds);
                    p.style = c.style;
                    if (p.value === undefined || p.value === "") {
                        p.value = "&#160;";
                    }
                    if (r.dirty && typeof r.modified[c.name] !== 'undefined') {
                        p.css += ' x-grid3-dirty-cell';
                    }
                    cb[cb.length] = ct.apply(p);
                }
            }
            var alt = [];
            if (stripe && ((rowIndex + 1) % 2 === 0)) {
                alt[0] = "x-grid3-row-alt";
            }
            if (r.dirty) {
                alt[1] = " x-grid3-dirty-row";
            }
            rp.cols = colCount;
            if (this.getRowClass) {
                alt[2] = this.getRowClass(r, rowIndex, rp, ds);
            }
            rp.alt = alt.join(" ");
            rp.cells = cb.join("");
            buf[buf.length] = !visible ? ts.rowHolder.apply(rp) : (onlyBody ? rb.apply(rp) : rt.apply(rp));
        }
        return buf.join("");
    },

    isRowRendered: function (index) {
        var row = this.getRow(index);
        return row && row.childNodes.length > 0;
    },

    syncScroll: function () {
        Ext.ux.grid.BufferView.superclass.syncScroll.apply(this, arguments);
        this.update();
    },

    // a (optionally) buffered method to update contents of gridview
    update: function () {
        if (this.scrollDelay) {
            if (!this.renderTask) {
                this.renderTask = new Ext.util.DelayedTask(this.doUpdate, this);
            }
            this.renderTask.delay(this.scrollDelay);
        } else {
            this.doUpdate();
        }
    },

    onRemove: function (ds, record, index, isUpdate) {
        Ext.ux.grid.BufferView.superclass.onRemove.apply(this, arguments);
        if (isUpdate !== true) {
            this.update();
        }
    },

    doUpdate: function () {
        if (this.getVisibleRowCount() > 0) {
            var g = this.grid,
                cm = g.colModel,
                ds = g.store,
                cs = this.getColumnData(),
                vr = this.getVisibleRows(),
                row;
            for (var i = vr.first; i <= vr.last; i++) {
                // if row is NOT rendered and is visible, render it
                if (!this.isRowRendered(i) && (row = this.getRow(i))) {
                    var html = this.doRender(cs, [ds.getAt(i)], ds, i, cm.getColumnCount(), g.stripeRows, true);
                    row.innerHTML = html;
                }
            }
            this.clean();
        }
    },

    // a buffered method to clean rows
    clean: function () {
        if (!this.cleanTask) {
            this.cleanTask = new Ext.util.DelayedTask(this.doClean, this);
        }
        this.cleanTask.delay(this.cleanDelay);
    },

    doClean: function () {
        if (this.getVisibleRowCount() > 0) {
            var vr = this.getVisibleRows();
            vr.first -= this.cacheSize;
            vr.last += this.cacheSize;

            var i = 0, rows = this.getRows();
            // if first is less than 0, all rows have been rendered
            // so lets clean the end...
            if (vr.first <= 0) {
                i = vr.last + 1;
            }
            for (var len = this.ds.getCount(); i < len; i++) {
                // if current row is outside of first and last and
                // has content, update the innerHTML to nothing
                if ((i < vr.first || i > vr.last) && rows[i].innerHTML) {
                    rows[i].innerHTML = '';
                }
            }
        }
    },

    removeTask: function (name) {
        var task = this[name];
        if (task && task.cancel) {
            task.cancel();
            this[name] = null;
        }
    },

    destroy: function () {
        this.removeTask('cleanTask');
        this.removeTask('renderTask');
        Ext.ux.grid.BufferView.superclass.destroy.call(this);
    },

    layout: function () {
        Ext.ux.grid.BufferView.superclass.layout.call(this);
        this.update();
    }
});


Ext.ux.CustomGrid = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
    colModel: null,
    instance: null,
    viewConfig: {
        //forceFit:true
    },
    onRender:function() {
        Ext.ux.CustomGrid.superclass.onRender.apply(this, arguments);
        this.store.client=this;
        this.store.load();
    },
    onWrite: function(result) {
        if(result.success) {
            //this.store.commitChanges();
        } else {
            this.selModel.selectRow(this.unsaved_row)
        }
    },
    initComponent: function(options) {
        options = options || {};
        var config = {
            frame:true,
            current_row: 0,
            unsaved_row: 0,
            tbar: [
            this.searchfield = new Ext.form.TextField({
                listeners: {
                    specialkey: {
                        fn: function(field, e){
                            if (e.getKey() == e.ENTER) {
                                this.searchAction()
                            }
                        },
                        scope: this
                    }
                }
            }),{
                xtype: 'tbseparator'
            },{
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchAction()
                },
                scope: this
            },
            this.searchClearButton = {
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    var grid = Ext.getCmp(this.id);
                    grid.searchfield.setValue('');
                    grid.store.baseParams.filter_value = '';
                    grid.store.reload();
                    this.resizeAction();
                },
                scope: this
            },{
                xtype: 'tbseparator'
            },{
                xtype: 'label',
                text: 'Всього:'
            },
            this.lb_total = new Ext.form.TextField({
                width: '60px'
            }),{
                xtype: 'tbseparator'
            },{
                xtype: 'label',
                text: 'Не в реєстрах:'
            },
            this.lb_unregistered = new Ext.form.TextField({
                xtype: 'textfield',
                width: '60px'
            }),{
                xtype: 'tbseparator'
            },{
                xtype: 'label',
                text: 'Не проведені:'
            },
            this.lb_unprocessed = new Ext.form.TextField({
                xtype: 'textfield',
                width: '60px'
            }),{
                xtype: 'tbseparator'
            }],
            bbar: this.pager = new Ext.PagingToolbar({
//                pageSize:  this.pageSize || 16,
                store: this.store
            }),
            listeners: {
                beforeclose: {
                    fn: function(obj) {
                        obj.hide()
                    }
                },
                beforedestroy: {
                    fn: function(e) {
                        return false;
                    }
                },
                afterrender: {
                    fn: function(e) {
                        var grid = Ext.getCmp(this.id);
                        grid.getView().dragZone.onBeforeDrag = function(el, e) {
                            if(grid.disableDragDrop) {
                                return false
                            }
                            var isValidDrag = true;
                            Ext.each(el.selections, function(row) {
                                if(row.data.locked) {
                                    isValidDrag = false;
                                }
                            });
                            return isValidDrag;
                        };
                        var GridDropTargetEl =  grid.getView().scroller.dom;
                        grid.GridDropTarget = new Ext.dd.DropTarget(GridDropTargetEl, {
                            ddGroup    : 'GridDD',
                            notifyDrop : function(ddSource, e, data){
                                if(grid.disableDragDrop) {
                                    return false
                                }
                                var records =  ddSource.dragData.selections;
                                Ext.each(records, ddSource.grid.store.remove, ddSource.grid.store);
                                grid.store.add(records);
                                Ext.each(records, function(r){
                                    var target = grid.store.baseParams.filter.category__pk || 0;
                                    MainApi.set_entry_category(r.id, target, function(response){
                                        grid.store.reload();
                                        ddSource.grid.store.reload();
                                        window.totalstab.store.reload();
                                        if(grid.update_stats) {
                                            grid.update_stats();
                                        }
                                        if(ddSource.grid.update_stats) {
                                            ddSource.grid.update_stats();
                                        }
                                        if(window.totalstab.update_stats) {
                                            window.totalstab.update_stats();
                                        }
                                    });
                                });
                                return true;
                            }
                        });
                        grid.resizeAction();
                    }
                },
                resize: {
                    fn: function(e) {
                        this.resizeAction();
                    }
                },
                rowcontextmenu: function(grid, index, event){
                     event.stopEvent();
                     Ext.ux.mnuContext.data = grid.store.getAt(index);
                     Ext.ux.mnuContext.showAt(event.xy);
                }

            },
            resizeAction: function() {
                var grid = Ext.getCmp(this.id);
                    var height = grid.getView().scroller.getHeight();
                    if(height>100) {
                        delete grid.pager.pageSize;
                        delete grid.pageSize;
                        grid.pager.pageSize = parseInt((height-10)/21);
                        $("#"+grid.pager.id).find('button.x-tbar-loading').click();
                    }
            },
            searchAction: function() {
                var grid = Ext.getCmp(this.id);
                grid.store.baseParams.filter_value = grid.searchfield.getValue();
                grid.store.reload();
                this.resizeAction();
            },
            enableDragDrop: true,
            ddGroup: "GridDD",
            sm: new Ext.grid.RowSelectionModel({
                singleSelect: false,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {

                        },
                        scope: this
                    }
                }
            })
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});


var entry_ds_model = Ext.data.Record.create([
    'id',
    'pid',
    'timestamp',
    'amount',
    'currency',
    'egrpou',
    'verbose_name',
    'account_num',
    'mfo',
    'descr',
    'processed'
]);


Ext.ux.Entry_store_config = {
    api: {
        read: EntryGrid.read,
        create: EntryGrid.foo,
        update: EntryGrid.foo,
        destroy: EntryGrid.foo
    },
    remoteSort: true,
    restful: true,
    autoLoad: false,
    autoSave: false,
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        idProperty: 'id',
        fields: [
            'id',
            'pid',
            'timestamp',
            'amount',
            'currency',
            'egrpou',
            'verbose_name',
            'account_num',
            'mfo',
            'descr',
            'processed',
            'statement_id',
            'category_id',
            'parent_id',
            'register_id',
            'locked'
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
};


Ext.ux.EntryStore = Ext.extend(Ext.data.DirectStore, {
    initComponent: function(options) {
        var config = Ext.ux.Entry_store_config;
        options = options || {};
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.EntryStore.superclass.initComponent.apply(this, arguments);
    }
});


var colModel = new Ext.grid.ColumnModel({
    columns: [
        {header: "Id", dataIndex: 'id', width:50, sortable: true},
        {header: "Pid", dataIndex: 'pid', sortable: true},
        {header: "Час", dataIndex: 'timestamp', width:120, sortable: true},
        {header: "Сума", dataIndex: 'amount', width:50, sortable: true},
        {header: "Валюта", dataIndex: 'currency', width:40, sortable: true},
        {header: "ЕГРПОУ", dataIndex: 'egrpou', width:80, sortable: true},
        {header: "Назва", dataIndex: 'verbose_name', width:200, sortable: true},
        {header: "Рахунок", dataIndex: 'account_num', sortable: true},
        {header: "МФО", dataIndex: 'mfo', sortable: true},
        {header: "Коментар", dataIndex: 'descr', sortable: true},
        {header: "Проведено", dataIndex: 'processed', sortable: true},
        {header: "Реєстр", dataIndex: 'register_id', sortable: true}
    ],
    defaults: {
        sortable: true,
        width: 100
    }
});


Ext.ux.EntryGrid = Ext.extend(Ext.ux.CustomGrid, {
    ds_model: entry_ds_model,
    title: 'Entry',
    stateful: true,
    stateId: 'stateGrid1',
    colModel: colModel,
    initComponent: function(options) {
        options = options || {};
        var config = {
            closable: false
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.EntryGrid.superclass.initComponent.apply(this, arguments);
    }
});


Ext.reg('ext:ux:entry-grid', Ext.ux.EntryGrid);


Ext.ux.TabPanel = Ext.extend(Ext.TabPanel,{
    initComponent: function(){
        var config = {
            frame:true,
            closable:false
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.TabPanel.superclass.initComponent.apply(this, arguments);
    }
});


Ext.ux.Category_store_config = {
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'new_cat_combo_store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        fields: [
            'id',
            'name',
            'svc_type',
            'source_id'
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    api: {
        read: MainApi.get_available_categories,
        create: EntryGrid.foo,
        update: EntryGrid.foo,
        destroy: EntryGrid.foo
    }
};

Ext.ux.NewCategoryStore = Ext.extend(Ext.data.DirectStore, {
    initComponent: function(options){
        var config = {};
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        options = options || {};
        Ext.apply(this, options);
        Ext.ux.new_cat_combo_store.superclass.initComponent.apply(this, arguments);
    }
});

//stst = new Ext.ux.new_cat_combo_store();

Ext.ux.NewCategorySelect = Ext.extend(Ext.form.ComboBox, {
    initComponent: function(options){
        var config = {
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        options = options || {};
        Ext.apply(this, options);
        Ext.ux.NewCategorySelect.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:cat-select', Ext.ux.NewCategorySelect);