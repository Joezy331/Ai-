import streamlit as st
import PyPDF2
from openai import OpenAI

# -----------------------------
# 页面基础设置
# -----------------------------

st.set_page_config(
    page_title="AI Resume Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# 初始化大模型（硅基流动）
# -----------------------------

client = OpenAI(
    api_key="sk-pmchycpgzryqpiwwhzsyaxkpoghapsnrxvqwxvzolxvkcjsh",
    base_url="https://api.siliconflow.cn/v1"
)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🤖 AI Resume Assistant")

    st.write("一个基于大模型的简历分析工具")

    st.write("### 功能")
    st.write("✅ PDF简历上传")
    st.write("✅ 岗位JD分析")
    st.write("✅ AI匹配评分")
    st.write("✅ 面试问题生成")

# -----------------------------
# 主页面
# -----------------------------

st.title("AI Resume Assistant")

st.header("Resume Analysis")

st.write("上传简历并输入岗位JD，AI会自动分析。")

# -----------------------------
# 上传PDF
# -----------------------------

uploaded_file = st.file_uploader(
    "上传你的简历 PDF",
    type="pdf",
    key="resume_uploader"
)

# -----------------------------
# JD输入框
# -----------------------------

job_description = st.text_area(
    "请输入岗位JD",
    height=250,
    key="job_description_input"
)

# -----------------------------
# 读取PDF内容
# -----------------------------

resume_text = ""

if uploaded_file:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text

    st.subheader("简历内容预览")

    st.text(resume_text[:2000])

# -----------------------------
# Analyze按钮
# -----------------------------

if st.button("Analyze Resume", key="analyze_button"):

    # 未上传PDF
    if not uploaded_file:

        st.warning("请先上传简历PDF")

    # 未输入JD
    elif not job_description:

        st.warning("请输入岗位JD")

    else:

        with st.spinner("AI正在分析中..."):

            # Prompt
            prompt = f"""
你是一名资深HR和AI产品经理面试官。

请根据岗位JD分析候选人简历。

请输出：

# 1. 匹配评分（0-100）

# 2. 候选人优势

# 3. 缺失技能

# 4. 简历优化建议

# 5. 可能出现的面试问题

请使用清晰Markdown格式输出。

岗位JD：
{job_description}

候选人简历：
{resume_text}
"""

            try:

                response = client.chat.completions.create(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7
                )

                answer = response.choices[0].message.content

                st.success("分析完成！")

                st.subheader("AI 分析结果")

                st.markdown(answer)

            except Exception as e:

                st.error(f"发生错误：{e}")