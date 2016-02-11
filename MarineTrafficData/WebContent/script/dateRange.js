function binarySearchGreaterThanDate(key, a) {
	//console.log("Calling..."+a.length);
	//console.log(a);
	var low = 0;
	var high = a.length - 1;
	var indexPos = -1;
	key = key.valueOf();
	if(a.length > 0 && (new Date(a[0])).valueOf() > key) {
		console.log("D : " + a[0] + " key : " + key)
		return 0;
	}
	while (high >= low) {
		//console.log("low : " + low+" high : " + high);
		var middle = parseInt((low + high) / 2);
		var date1 = (new Date(a[middle])).valueOf();
		//console.log("Middle : "+middle+" date : " + date1);
		if (date1 == key) {
			indexPos = middle;
			break;
		}
		if(high == low) {
			while(high < a.length) {
				var date2 = (new Date(a[high])).valueOf();
				if(date2 > key) {
					indexPos = high;
					break;
				}
				high++;
			}
			break;
		}
		if (date1 < key) {
			low = middle + 1;
		}
		if (date1 > key) {
			high = middle - 1;
		}
	}
	//console.log("Index : " + indexPos);
	//console.log("valuevvvvv : " + a[indexPos]);
	return indexPos;
}
function binarySearchLessThanDate(key, a) {
	//console.log("Calling..."+a.length);
	//console.log(a);
	var low = 0;
	var high = a.length - 1;
	var indexPos = -1;
	key = key.valueOf();
	while (high >= low) {
		var middle = parseInt((low + high) / 2);
		var date1 = (new Date(a[middle])).valueOf();
		if (date1 == key) {
			indexPos = middle;
			break;
		}
		if(high == low) {
			while(high >= 0) {
				var date2 = (new Date(a[high])).valueOf();
				if(date2 < key) {
					indexPos = high;
					break;
				}
				high--;
			}
			break;
		}
		if (date1 < key) {
			low = middle + 1;
		}
		if (date1 > key) {
			high = middle - 1;
		}
	}
	//console.log("Index : " + indexPos);
	//console.log("valuevvvvv : " + a[indexPos]);
	return indexPos;
}