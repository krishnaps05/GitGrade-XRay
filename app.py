import streamlit as st
from gitgradexray import *

st.set_page_config(page_title="GitGrade X-Ray", layout="centered")

st.title("🔍 GitGrade X-Ray")
st.write("AI-powered GitHub Repository Analyzer")

repo_url = st.text_input("Enter a public GitHub repository URL")

if st.button("Analyze Repository"):
    if not repo_url:
        st.warning("Please enter a repository URL")
    else:
        with st.spinner("Analyzing repository..."):
            try:
                repo = fetch_repo_info(repo_url)

                st.subheader("📌 Repository Information")
                st.write("**Name:**", repo.name)
                st.write("**Description:**", repo.description)
                st.write("**Stars:**", repo.stargazers_count)
                st.write("**Forks:**", repo.forks_count)
                st.write("**Open Issues:**", repo.open_issues_count)
                st.write("**Primary Language:**", repo.language)

                r, rf = analyze_readme(repo)
                c, cf = analyze_commits(repo)
                t, tf = analyze_tests(repo)

                feedback = rf + cf + tf
                score, level = generate_health_score(r, c, t)

                st.subheader("📊 Repository Health Score")
                st.progress(score)
                st.write(f"**Score:** {score}/100")
                st.write(f"**Developer Level:** {level}")

                st.subheader("🧑‍💼 Recruiter Verdict")
                st.success(recruiter_verdict(score)) if score >= 60 else st.error(recruiter_verdict(score))

                st.subheader("🧠 AI Mentor Feedback")
                if feedback:
                    for f in feedback:
                        st.write("•", f)
                else:
                    st.success("Repository is well structured")

                st.subheader("🚀 Career Roadmap")
                for f in feedback:
                    st.write("➡ Improve:", f)

            except Exception as e:
                st.error(f"Error: {e}")
