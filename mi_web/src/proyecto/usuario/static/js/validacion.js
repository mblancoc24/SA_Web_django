function change() {
  var selectValue = document.getElementById("tipo");
  var input = document.getElementById("identificacion");
  var telefono = document.getElementById("telefono");
  telefono.oninput = function () {
    this.value = this.value.replace(/[^0-9]/g, "");
  };
  if (selectValue.value === "Cédula") {
    input.oninput = function () {
      this.value = this.value.replace(/[^0-9]/g, "");
    };
    input.value = "";
    input.removeAttribute("disabled");
    input.setAttribute("minLength", "9");
    input.setAttribute("maxLength", "9");
  } else if (selectValue.value === "Dimex") {
    input.oninput = function () {
      this.value = this.value.replace(/[^0-9]/g, "");
    };
    input.value = "";
    input.removeAttribute("disabled");
    input.setAttribute("minLength", "11");
    input.setAttribute("maxLength", "12");
  } else if (selectValue.value === "Pasaporte") {
    input.oninput = null;
    input.value = "";
    input.removeAttribute("disabled");
    input.setAttribute("minLength", "9");
    input.setAttribute("maxLength", "20");
  } else if (selectValue.value === "Refugiado") {
    input.oninput = function () {
      this.value = this.value.replace(/[^0-9]/g, "");
    };
    input.value = "";
    input.removeAttribute("disabled");
    input.setAttribute("minLength", "12");
    input.setAttribute("maxLength", "12");
  } else if (selectValue.value === "Permiso") {
    input.oninput = null;
    input.value = "";
    input.removeAttribute("disabled");
  } else if (selectValue.value === "Cédula Residente") {
    input.oninput = function () {
      this.value = this.value.replace(/[^0-9]/g, "");
    };
    input.value = "";
    input.removeAttribute("disabled");
    input.setAttribute("minLength", "12");
    input.setAttribute("maxLength", "12");
  }
}

$(document).ready(function () {
  $("#tipo").change(function () {
    $("#nombre").val("");
    $("#primerapellido").val("");
    $("#segundoapellido").val("");
    $("#telefono").val("");
    $("#fechanacimiento").val("");
    $("#correo").val("");
    $("#password1").val("");
    $("#password2").val("");
  });

  const password1 = $("#password1");
  const password2 = $("#password2");

  function validatePasswords() {
    if (password1.val() !== password2.val()) {
      password2[0].setCustomValidity("Contraseña no coinciden");
    } else {
      password2[0].setCustomValidity("");
    }
  }

  password1.on("input", validatePasswords);
  password2.on("input", validatePasswords);

  $("#identificacion").on("keydown", (e) => {
    if (e.which === 8) {
      var nombre = document.getElementById("nombre");
      var primer = document.getElementById("primerapellido");
      var segundo = document.getElementById("segundoapellido");
      nombre.value = "";
      nombre.removeAttribute("readonly");
      primer.value = "";
      primer.removeAttribute("readonly");
      segundo.value = "";
      segundo.removeAttribute("readonly");
    }
  });
});