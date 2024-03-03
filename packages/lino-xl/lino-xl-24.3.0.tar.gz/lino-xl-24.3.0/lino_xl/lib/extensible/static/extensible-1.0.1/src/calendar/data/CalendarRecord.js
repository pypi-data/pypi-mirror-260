/*!
 * Extensible 1.0.1
 * Copyright(c) 2010-2011 Extensible, LLC
 * licensing@ext.ensible.com
 * http://ext.ensible.com
 */
/**
 * @class Ext.ensible.cal.CalendarRecord
 * @extends Ext.data.Record
 * <p>This is the {@link Ext.data.Record Record} specification for calendar items used by the
 * {@link Ext.ensible.cal.CalendarPanel CalendarPanel}'s calendar store. If your model fields 
 * are named differently you should update the <b>mapping</b> configs accordingly.</p>
 * <p>The only required fields when creating a new calendar record instance are CalendarId and
 * Title.  All other fields are either optional or will be defaulted if blank.</p>
 * <p>Here is a basic example for how to create a new record of this type:<pre><code>
rec = new Ext.ensible.cal.CalendarRecord({
    CalendarId: 5,
    Title: 'My Holidays',
    Description: 'My personal holiday schedule',
    ColorId: 3
});
</code></pre>
 * If you have overridden any of the record's data mappings via the {@link Ext.ensible.cal.CalendarMappings CalendarMappings} object
 * you may need to set the values using this alternate syntax to ensure that the fields match up correctly:<pre><code>
var M = Ext.ensible.cal.CalendarMappings;

rec = new Ext.ensible.cal.CalendarRecord();
rec.data[M.CalendarId.name] = 5;
rec.data[M.Title.name] = 'My Holidays';
rec.data[M.Description.name] = 'My personal holiday schedule';
rec.data[M.ColorId.name] = 3;
</code></pre>
 * @constructor
 * @param {Object} data (Optional) An object, the properties of which provide values for the new Record's
 * fields. If not specified the {@link Ext.data.Field#defaultValue defaultValue}
 * for each field will be assigned.
 * @param {Object} id (Optional) The id of the Record. The id is used by the
 * {@link Ext.data.Store} object which owns the Record to index its collection
 * of Records (therefore this id should be unique within each store). If an
 * id is not specified a {@link #phantom}
 * Record will be created with an {@link #Record.id automatically generated id}.
 */
Ext.ensible.cal.CalendarRecord = Ext.extend(Ext.data.Record, {
    fields: new Ext.util.MixedCollection(false, function(field){
        return field.name;
    })
});

/**
 * Reconfigures the default record definition based on the current {@link Ext.ensible.cal.CalendarMappings CalendarMappings}
 * object. See the header documentation for {@link Ext.ensible.cal.CalendarMappings} for complete details and 
 * examples of reconfiguring a CalendarRecord.
 * @method create
 * @static
 * @return {Function} The updated CalendarRecord constructor function
 */
Ext.ensible.cal.CalendarRecord.reconfigure = function(){
    var C = Ext.ensible.cal,
        M = C.CalendarMappings,
        proto = C.CalendarRecord.prototype,
        fields = [];
    
    for(prop in M){
        if(M.hasOwnProperty(prop)){
            fields.push(M[prop]);
        }
    }
    proto.fields.clear();
    for(var i = 0, len = fields.length; i < len; i++){
        proto.fields.add(new Ext.data.Field(fields[i]));
    }
    return C.CalendarRecord;
};

// Create the default definition now:
Ext.ensible.cal.CalendarRecord.reconfigure();