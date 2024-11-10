$(document).ready(function() {

    // Table handling
    $(".table-search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".vehicle-table > tbody > tr > td.searchable").filter(function() {
          $(this).parent().toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $(".table-search").val("");

    // Vehicle modal
    const getData = async (vid) => {
        const url = "/api/vehicles/" + vid;
        const response = await fetch(url);
        return await response.json();
    }

  // Functions to open and close a modal
  async function openModal(el, vid) {
    $("#card-vehiclename").text("");
    $("#card-vehicleclass").text("");
    $("#card-vehicleimage").attr("src", "");
    $("#card-vehicleimage").attr("alt", "");
    $("#card-weapontable tbody").empty();
    $(el).addClass('is-active')
    const data = await getData(vid);
    $("#card-vehiclename").text(data.name);
    $("#card-vehicleclass").text(data.class_name);
    $("#card-vehicleimage").attr("src", data.image);
    $("#card-vehicleimage").attr("alt", data.name);
    $(data.armaments).each(async (_ix, weapon) => {
        const has_rounds = weapon.ammo.rounds;
        var ammo = "";
        if (has_rounds !== undefined && has_rounds !== false) {
            ammo = `${weapon.ammo.rounds}`;
        } else {
            $(weapon.ammo.options).each(async (_ix, load) => {
                ammo = `${ammo}${load.name}: ${load.rounds}<br>`
                console.log(load);
            });
        }
        $('#card-weapontable tbody').append(`<tr><td>${weapon.name}</td><td>${weapon.model}</td><td>${weapon.caliber}</td><td>${ammo}</td></tr>`);
      });
  }

  function closeModal(el) {
    $(el).removeClass('is-active');
  }

  function closeAllModals() {
    $('.modal').each((_ix, modal) => {
        closeModal(modal);
      });
    }

  // Add a click event on buttons to open a specific modal
  $(".js-modal-trigger").each((_ix, trigger) => {
    const modal = trigger.dataset.target;
    const vehicleid = trigger.dataset.vehicleid;
    const target = document.getElementById(modal);

    $(trigger).on("click", () => {
      openModal(target, vehicleid);
    });
  });

  // Add a click event on various child elements to close the parent modal
  $(".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button").each((_ix, close) => {
    const target = close.closest('.modal');

    $(close).on('click', () => {
      closeModal(target);
    });
  });

  // Add a keyboard event to close all modals
  $(document).on("keydown", (event) => {
    if(event.key === "Escape") {
      closeAllModals();
    }
  });
});
