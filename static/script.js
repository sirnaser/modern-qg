document.addEventListener("DOMContentLoaded", () => {
  const modelSelectContent = document.getElementById("modelSelectContent");
  const modelSelectTex = document.getElementById("modelSelectTex");
  const languageSelectContent = document.getElementById("languageSelectContent");
  const languageSelectTex = document.getElementById("languageSelectTex");
  const formContent = document.getElementById("formContent");
  const formTex = document.getElementById("formTex");
  const contentInput = document.getElementById("contentInput");
  const texFileInput = document.getElementById("texFileInput");
  const statusArea = document.getElementById("statusArea");

  // Fetch available models from backend
  async function fetchModels() {
    try {
      const res = await fetch("/api/models");
      if (!res.ok) throw new Error("Failed to load models");
      const models = await res.json();
      return models;
    } catch (err) {
      console.error(err);
      statusArea.textContent = "خطا در دریافت مدل‌ها از سرور.";
      return [];
    }
  }

  // Populate model select elements
  function populateModelSelect(models, selectElement) {
    selectElement.innerHTML = "";
    models.forEach((model, idx) => {
      const opt = document.createElement("option");
      opt.value = model.name;
      opt.textContent = model.display_name || model.name;
      selectElement.appendChild(opt);
    });
  }

  // Initialize selects
  async function initializeSelectors() {
    const models = await fetchModels();
    if (models.length === 0) return;
    populateModelSelect(models, modelSelectContent);
    populateModelSelect(models, modelSelectTex);
  }

  // Show status messages
  function setStatus(msg, isError = false) {
    statusArea.textContent = msg;
    statusArea.style.color = isError ? "red" : "#2c3e50";
  }

  // Handle form submit for content input
  formContent.addEventListener("submit", async (e) => {
    e.preventDefault();
    const content = contentInput.value.trim();
    if (!content) {
      setStatus("لطفا متن محتوا را وارد کنید.", true);
      return;
    }
    const model_type = modelSelectContent.value;
    const language = languageSelectContent.value;

    setStatus("در حال ارسال درخواست و تولید سوالات...");

    try {
      const res = await fetch("/api/generate_questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, model_type, language }),
      });
      if (!res.ok) throw new Error("خطا در سرور");
      const data = await res.json();
      setStatus(`سوالات تولید شد.\nبرای دانلود روی لینک زیر کلیک کنید:\n${window.location.origin}/download/${data.file_path}`);
    } catch (err) {
      console.error(err);
      setStatus("خطا در تولید سوالات.", true);
    }
  });

  // Handle form submit for tex file upload
  formTex.addEventListener("submit", async (e) => {
    e.preventDefault();
    const files = texFileInput.files;
    if (!files || files.length === 0) {
      setStatus("لطفا فایل TeX نمونه سوالات را انتخاب کنید.", true);
      return;
    }
    const model_type = modelSelectTex.value;
    const language = languageSelectTex.value;

    setStatus("در حال ارسال فایل و تولید سوالات مشابه...");

    try {
      const formData = new FormData();
      formData.append("file", files[0]);
      formData.append("model_type", model_type);
      formData.append("language", language);

      const res = await fetch("/api/generate_similar_questions", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("خطا در سرور");
      const data = await res.json();
      setStatus(`سوالات مشابه تولید شد.\nبرای دانلود روی لینک زیر کلیک کنید:\n${window.location.origin}/download/${data.file_path}`);
    } catch (err) {
      console.error(err);
      setStatus("خطا در تولید سوالات مشابه.", true);
    }
  });

  initializeSelectors();
});
