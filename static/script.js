const fileInput = document.getElementById('file');
const langSel   = document.getElementById('lang');
const modelSel  = document.getElementById('model');
const btn       = document.getElementById('generate');
const statusEl  = document.getElementById('status');
const downEl    = document.getElementById('download');

function setStatus(txt){statusEl.textContent = txt;}

btn.onclick = async () => {
  if(!fileInput.files.length){return alert("لطفاً فایل وارد کنید");}
  setStatus("⏳ در حال بارگذاری فایل و تولید سؤال…");
  const fd = new FormData();
  fd.append("file", fileInput.files[0]);
  fd.append("language", langSel.value);
  fd.append("model", modelSel.value);
  const res = await fetch("/generate", {method:"POST", body:fd});
  if(!res.ok){setStatus("❌ خطا در تولید سؤال"); return;}
  const data = await res.json();
  setStatus(`✅ آماده! (مدل: ${data.model_used})`);
  downEl.href = `/download/${data.file_path}`;
  downEl.style.display="inline-block";
};
document.getElementById("file").addEventListener("change", () => {
  const file = document.getElementById("file").files[0];
  document.getElementById("status").textContent = file ? `فایل انتخاب شده: ${file.name}` : "فایلی انتخاب نشده";
});
