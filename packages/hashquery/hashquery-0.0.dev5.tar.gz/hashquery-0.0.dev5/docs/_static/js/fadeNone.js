$(document).ready(function () {
  $('.sig-param .n .pre:contains("None")').addClass("hb-param-none");

  $('.sig-param:has(.default_value:contains("None"))').addClass(
    "hb-param-none-default",
  );
});
