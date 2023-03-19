$(document).ready(function(){
  $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
  });

  // Sorting from: https://orangeable.com/javascript/jquery-table-sorting
  $(document).on("click", "table thead tr th:not(.no-sort)", function() {
  	var table = $(this).parents("table");
  	var rows = $(this).parents("table").find("tbody tr").toArray().sort(TableComparer($(this).index()));
  	var dir = ($(this).hasClass("sort-asc")) ? "desc" : "asc";

  	if (dir == "desc") {
  		rows = rows.reverse();
  	}

  	for (var i = 0; i < rows.length; i++) {
  		table.append(rows[i]);
  	}

  	table.find("thead tr th").removeClass("sort-asc").removeClass("sort-desc");
  	$(this).removeClass("sort-asc").removeClass("sort-desc") .addClass("sort-" + dir);
  });

  function TableComparer(index) {
  	return function(a, b) {
  		var val_a = TableCellValue(a, index);
  		var val_b = TableCellValue(b, index);
  		var result = ($.isNumeric(val_a) && $.isNumeric(val_b)) ? val_a - val_b : val_a.toString().localeCompare(val_b);

  		return result;
  	}
  }

  function TableCellValue(row, index) {
  	return $(row).children("td").eq(index).text();
  }
  // end table sort


});
