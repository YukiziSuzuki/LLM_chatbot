import streamlit as st
import pandas as pd
from groq import Groq

def main():
    st.title("AIとのチャットボット")
    
    # ローカルのExcelファイルパスを指定
    excel_file_path = r"C:\Users\aobas\Downloads\ナレッジ共有.xlsx"
    # APIキーの入力
    api_key = "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"

    # ユーザーのメッセージを入力
    user_input = st.text_input("メッセージを入力してください")

    if st.button("送信"):
        if api_key and user_input:
            try:
                # 指定したパスのExcelファイルを読み込む
                df = pd.read_excel(excel_file_path, engine='openpyxl')

                # Excelデータを表示
                st.write("Excelファイルの内容:")
                st.write(df)

                # データフレームを文字列に変換してLLMに送信する準備
                excel_data_str = df.to_csv(index=False)

                # Groqクライアントの作成
                client = Groq(api_key=api_key)

                # ユーザーのメッセージとExcelデータを含むメッセージを生成
                prompt = (
                    f"以下のデータは企画会議におけるトラブルシューティングをまとめたものです:\n\n"
                    f"{excel_data_str}\n\n"
                    f"このデータに基づいて回答を行ってください:\n"
                    f"この企画会議には学生とメンターがいます:\n"
                    f"{user_input}"
                    f"answer please in japanese:\n"
                )

                # チャットの実行
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "あなたは役に立つアシスタントです。"},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192"
                )

                # チャットの結果を表示
                bot_response = chat_completion.choices[0].message.content
                st.text("AIの返答: " + bot_response)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.error("APIキーおよびメッセージを入力してください")

if __name__ == "__main__":
    main()
