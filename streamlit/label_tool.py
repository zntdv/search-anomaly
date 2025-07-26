import streamlit as st
import pandas as pd
import os
import altair as alt

# === Параметры ===
WINDOWS_DIR = "split_windows"
LABELS_FILE = "labels.csv"
MAX_POINTS = 1000  # максимум точек на графике

LABEL_OPTIONS = {
    0: "0 — нет дефекта",
    1: "1 — дефект подшипника",
    2: "2 — дисбаланс",
    3: "3 — расцентровка",
    4: "4 — прочее"
}

# === Инициализация интерфейса ===
st.set_page_config(page_title="Разметка сигналов", layout="wide")
st.title("🧠 Разметка токовых сигналов")

# === Загрузка списка файлов ===
if not os.path.exists(WINDOWS_DIR):
    st.error(f"Папка {WINDOWS_DIR} не найдена.")
    st.stop()

window_files = sorted([f for f in os.listdir(WINDOWS_DIR) if f.endswith(".csv")])

# === Загрузка уже размеченных меток ===
if os.path.exists(LABELS_FILE):
    labels_df = pd.read_csv(LABELS_FILE)
    labeled_files = set(labels_df["filename"])
else:
    labels_df = pd.DataFrame(columns=["filename", "label"])
    labeled_files = set()

# === Фильтрация неразмеченных окон ===
unlabeled_files = [f for f in window_files if f not in labeled_files]
total_files = len(window_files)
done_files = len(labeled_files)

# === Прогресс ===
st.progress(done_files / total_files if total_files else 0)
st.write(f"📦 Размечено: {done_files} / {total_files}")

# === Разметка следующего окна ===
if unlabeled_files:
    selected_file = unlabeled_files[0]
    file_path = os.path.join(WINDOWS_DIR, selected_file)
    df = pd.read_csv(file_path)

    # Ограничение точек для отображения
    if len(df) > MAX_POINTS:
        df = df.iloc[::20].copy()

    # Подготовка данных для Altair
    df["index"] = df.index
    df_melt = df.melt(id_vars=["index"], value_vars=["current_R", "current_S", "current_T"],
                      var_name="Фаза", value_name="Ток")

    chart = alt.Chart(df_melt).mark_line().encode(
        x="index:Q",
        y="Ток:Q",
        color="Фаза:N"
    ).properties(width=800, height=400)

    st.subheader(f"📈 График сигнала: {selected_file}")
    st.altair_chart(chart, use_container_width=True)

    # Метка
    st.subheader("📝 Присвой метку")
    label_index = st.selectbox("Тип дефекта:", list(LABEL_OPTIONS.keys()), format_func=lambda x: LABEL_OPTIONS[x])

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("✅ Сохранить метку"):
            new_row = pd.DataFrame([{"filename": selected_file, "label": label_index}])
            labels_df = pd.concat([labels_df, new_row], ignore_index=True)
            labels_df.to_csv(LABELS_FILE, index=False)
            st.success(f"Сохранено: {LABEL_OPTIONS[label_index]}")
            st.session_state.skip_to_next = True

    with col2:
        if st.button("⏭️ Пропустить"):
            st.info("Окно пропущено.")
            st.experimental_rerun()
else:
    st.success("🎉 Все окна размечены!")

if "skip_to_next" in st.session_state and st.session_state.skip_to_next:
    st.session_state.skip_to_next = False
    st.experimental_rerun()
