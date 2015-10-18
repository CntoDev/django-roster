var CNTOUtils = CNTOUtils || {};

CNTOUtils.padDigits = function(number, digits) {
    var digitString = String(number);
    while (digitString.length < digits) {
        digitString = "0" + digitString;
    }

    return digitString;
};

CNTOUtils.getPKFromElement = function(memberElement) {
    var memberIdString = memberElement.parent().parent().attr("id");
    return parseInt(memberIdString.split("-")[1]);
};