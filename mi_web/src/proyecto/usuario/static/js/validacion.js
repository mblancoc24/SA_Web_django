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
  $('#exampleModalCenter').modal('show');
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

  const password1 = $("#password1");
  const password2 = $("#password2");
  password1.on("input", validatePasswords);
  password2.on("input", validatePasswords);
  $('.select2').select2();
});

function validatePasswords() {
  const passwordInput = document.getElementById('password1');
  const passwordInput2 = document.getElementById('password2');
  const password = passwordInput.value;
  const password2 = passwordInput2.value;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_.:;,\-\+\]\[\}\{\¡\¿\'\?=\´~\"!°¬|])[A-Za-z\d!@#$%^&*()_.:;,\-\+\]\[\}\{\¡\¿\'\?=\´~\"!°¬|]{8,}$/;

  if (password !== password2) {
    passwordInput2.setCustomValidity("Las contraseñas no coinciden");
  } else if (!passwordPattern.test(password)) {
    passwordInput2.setCustomValidity("La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.");
  } else {
    passwordInput2.setCustomValidity("");
  }
}