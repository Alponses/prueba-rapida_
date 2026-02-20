(function ($) {
  const DATATABLE_LANG = "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json";

  function parseOrderAttr(attr) {
    if (!attr) return [];
    try {
      return JSON.parse(attr);
    } catch (e) {
      return [];
    }
  }

  function initDataTables() {
    if (!$.fn.DataTable) return;

    $("[data-datatable]").each(function () {
      const $table = $(this);
      if ($table.data("dt-init")) return;

      const emptyText = $table.data("empty") || "Sin registros";
      const pageLength = parseInt($table.data("page-length"), 10) || 10;
      const order = parseOrderAttr($table.data("order"));

      $table.DataTable({
        language: { url: DATATABLE_LANG, emptyTable: emptyText },
        pageLength,
        lengthChange: false,
        autoWidth: false,
        responsive: true,
        order,
      });

      $table.data("dt-init", true);
    });
  }

  function initTooltips() {
    if ($.fn.tooltip) {
      $('[data-toggle="tooltip"]').tooltip({ boundary: "window" });
    }
  }

  function persistSidebarState() {
    const key = "sidebar-collapsed";
    const $body = $("body");
    const saved = localStorage.getItem(key);
    if (saved === "true") {
      $body.addClass("sidebar-collapse");
    }
    $("[data-widget='pushmenu']").on("click", function () {
      const willCollapse = !$body.hasClass("sidebar-collapse");
      localStorage.setItem(key, willCollapse ? "true" : "false");
    });
  }

  $(function () {
    initDataTables();
    initTooltips();
    persistSidebarState();
  });

  // Expose for manual re-init after dynamic DOM updates
  window.GabosUI = { initDataTables };
})(jQuery);
