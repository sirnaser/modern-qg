function logStatus(message) {
  const statusArea = document.getElementById("statusArea");
  const timestamp = new Date().toLocaleTimeString();
  const entry = `[${timestamp}] ${message}\n`;
  statusArea.textContent += entry;
  statusArea.scrollTop = statusArea.scrollHeight;
}

// Load available models into dropdowns
async function loadModels() {
  try {
    const response = await fetch("/api/models");
    const data = await response.json();

    const selects = [document.getElementById("modelSelectContent"), document.getElementById("modelSelectTex")];
    for (const select of selects) {
      select.innerHTML = "";

      const autoOption = document.createElement("option");
      autoOption.value = "auto";
      autoOption.textContent = "انتخاب خودکار مدل";
      select.appendChild(autoOption);

      data.models.forEach((model) => {
        const option = document.createElement("option");
        option.value = model;
        option.textContent = model.replace(/\.gguf$/, "").replace(/-/g, " ");
        select.appendChild(option);
      });
    }

    logStatus("مدل‌ها با موفقیت بارگذاری شدند.");
  } catch (error) {
    logStatus("خطا در بارگذاری مدل‌ها: " + error.message);
  }
}

// Handle sending form data and downloading result
async function handleFormSubmission(formId, fileInputId, modelSelectId, languageSelectId, endpoint) {
  const fileInput = document.getElementById(fileInputId);
  const modelSelect = document.getElementById(modelSelectId);
  const languageSelect = document.getElementById(languageSelectId);

  const file = fileInput.files[0];
  let model = modelSelect.value;
  const language = languageSelect.value;

  if (!file) {
    logStatus("⚠️ فایل انتخاب نشده است.");
    return;
  }

  logStatus(`📁 فایل "${file.name}" انتخاب شد.`);
  logStatus(`🌐 زبان خروجی انتخاب‌شده: ${language}`);
  logStatus(`🤖 مدل انتخاب‌شده: ${model === "auto" ? "انتخاب خودکار" : model}`);

  // If user selected "auto", send file to /api/select-model
  if (model === "auto") {
    logStatus("🔍 در حال انتخاب خودکار مدل...");
    const autoForm = new FormData();
    autoForm.append("file", file);
    autoForm.append("language", language);

    try {
      const autoResponse = await fetch("/api/select-model", {
        method: "POST",
        body: autoForm,
      });
      const autoData = await autoResponse.json();
      model = autoData.selected_model;
      logStatus(`✅ مدل به‌صورت خودکار انتخاب شد: ${model}`);
    } catch (error) {
      logStatus("❌ خطا در انتخاب خودکار مدل: " + error.message);
      return;
    }
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("model_name", model);
  formData.append("language", language);

  logStatus("📤 در حال ارسال فایل به سرور...");

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.result) {
      logStatus("✅ سوالات تولید شدند. در حال دانلود فایل خروجی...");
      const blob = new Blob([data.result], { type: "application/x-tex" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "questions.tex";
      a.click();
      logStatus("📥 فایل .tex دانلود شد.");
    } else {
      throw new Error(data.error || "پاسخ نامعتبر از سرور.");
    }
  } catch (error) {
    logStatus("❌ خطا در دریافت پاسخ از مدل: " + error.message);
  }
}

// Bind form handlers to forms
function setupFormHandlers() {
  document.getElementById("formContent").addEventListener("submit", function (e) {
    e.preventDefault();
    handleFormSubmission("formContent", "mdFileInput", "modelSelectContent", "languageSelectContent", "/api/generate-from-md");
  });

  document.getElementById("formTex").addEventListener("submit", function (e) {
    e.preventDefault();
    handleFormSubmission("formTex", "texFileInput", "modelSelectTex", "languageSelectTex", "/api/generate-from-tex");
  });

  // Track changes
  document.getElementById("mdFileInput").addEventListener("change", () => {
    const file = document.getElementById("mdFileInput").files[0];
    if (file) logStatus(`📁 فایل جدید انتخاب شد: ${file.name}`);
  });

  document.getElementById("texFileInput").addEventListener("change", () => {
    const file = document.getElementById("texFileInput").files[0];
    if (file) logStatus(`📁 فایل جدید انتخاب شد: ${file.name}`);
  });

  document.getElementById("modelSelectContent").addEventListener("change", (e) => {
    logStatus(`🤖 مدل محتوای درسی تغییر یافت: ${e.target.value}`);
  });

  document.getElementById("modelSelectTex").addEventListener("change", (e) => {
    logStatus(`🤖 مدل نمونه سوال تغییر یافت: ${e.target.value}`);
  });

  document.getElementById("languageSelectContent").addEventListener("change", (e) => {
    logStatus(`🌐 زبان محتوای درسی تغییر یافت به: ${e.target.value}`);
  });

  document.getElementById("languageSelectTex").addEventListener("change", (e) => {
    logStatus(`🌐 زبان نمونه سوال تغییر یافت به: ${e.target.value}`);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadModels();
  setupFormHandlers();
});
