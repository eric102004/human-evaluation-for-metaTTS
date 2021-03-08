function doGet(e) {
	var params = e.parameter;

	var SpreadSheet = SpreadsheetApp.openById("1G10NWfG6f1SN7gwYiGL5n7ZjpwSgm0gYIRv6MyIuK24");
	var Sheet = SpreadSheet.getSheets()[params.formid-1];
	var LastRow = Sheet.getLastRow();

	Sheet.getRange(LastRow+1, 1).setValue(params.name);
	Sheet.getRange(LastRow+1, 2).setValue(params.mail);
	Sheet.getRange(LastRow+1, 3).setValue(params.formid);
  /*
  Sheet.getRange(LastRow+1, 1).setValue('name');
	Sheet.getRange(LastRow+1, 2).setValue('mail');
	Sheet.getRange(LastRow+1, 3).setValue('formid');
  */
	for (var i = 1; i <= 20; i++) {
		Sheet.getRange(LastRow+1, 3+i).setValue(params["q" + i.toString()]);
	}


	return ContentService.createTextOutput(params.thank);
  //return ContentService.createTextOutput('called');
}
