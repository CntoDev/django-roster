var CNTOUtils = CNTOUtils || {};

CNTOUtils.padDigits = function(number, digits) {
    var digitString = String(number);
    while (digitString.length < digits) {
        digitString = "0" + digitString;
    }

    return digitString;
};
