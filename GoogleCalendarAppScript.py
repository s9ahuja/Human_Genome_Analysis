function scheduleShifts() {
var spreadsheet = SpreadsheetApp.getActiveSheet();
var eventCal = CalendarApp.getCalendarById("48b4bm4ng4aeskv3hfrpc5vt0c@group.calendar.google.com");

var startRow = 4;  // First row of data to process - 2 exempts my header rowvar numRows = sheet.getLastRow();   // Number of rows to process
var numRows = spreadsheet.getLastRow();   // Number of rows to process
var numColumns = spreadsheet.getLastColumn();
var dataRange = spreadsheet.getRange(startRow, 1, numRows-1, numColumns);
var data = dataRange.getValues();
var complete = "Sign in"
for (var i = 0; i < data.length; ++i) 
{
    var shift = data[i];
    var startTime = shift[3];
    var endTime = shift[4];
    var HorM = shift[2];
    var email = shift[1];
    var name = shift[0];
    if (name && startTime && endTime) {  // Added
    if (eventCal.getEvents(startTime, endTime).length == 0) {  // Added
      eventCal.createEvent(name, startTime, endTime, {description: email + '\r' + HorM }); 
    }
  }
}
}
    