import io
import html
import hashlib
from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="Quality Intelligence | 결함 예측",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# 2. 프리미엄 UI CSS
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #0F1C2E;
        --navy-2: #1A2F4A;
        --blue: #2B5A8A;
        --blue-soft: #E8F0F8;
        --text: #1E2A3A;
        --muted: #5B6B7C;
        --border: #E2E8F0;
        --surface: #FFFFFF;
        --bg: #F4F6F9;
        --green: #1F7A5A;
        --green-soft: #E6F5EF;
        --red: #B83B3B;
        --red-soft: #FCEAEA;
        --shadow: 0 1px 3px rgba(15,28,46,0.04), 0 4px 16px rgba(15,28,46,0.06);
        --shadow-hover: 0 4px 20px rgba(15,28,46,0.10);
        --radius: 12px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .qi-header {
        background: linear-gradient(135deg, #0F1C2E 0%, #1A2F4A 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        color: white;
        box-shadow: var(--shadow);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
    }

    .qi-header-left {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .qi-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        color: #A8C5E2;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.2px;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
    }

    .qi-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin: 0;
        color: #FFFFFF;
        line-height: 1.25;
    }

    .qi-subtitle {
        font-size: 13px;
        color: #8BA3BC;
        margin: 0;
        font-weight: 400;
    }

    .qi-header-right {
        text-align: right;
        flex-shrink: 0;
    }

    .qi-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(31,122,90,0.2);
        border: 1px solid rgba(31,122,90,0.35);
        color: #6EE7B7;
        font-size: 12px;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 8px;
    }

    .qi-status-dot {
        width: 7px;
        height: 7px;
        background: #34D399;
        border-radius: 50%;
        box-shadow: 0 0 0 3px rgba(52,211,153,0.25);
    }

    .section-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.6px;
        color: #7A8B9E;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px 22px;
        min-height: 108px;
        box-shadow: var(--shadow);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        border-color: #C5D4E4;
        box-shadow: var(--shadow-hover);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px;
    }

    [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF;
        border: 1.5px dashed #B0C4D8;
        border-radius: 12px;
        padding: 28px 20px;
        transition: border-color 0.2s, background 0.2s;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--blue);
        background: #F7FAFD;
    }

    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        min-height: 44px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.2px;
        transition: all 0.18s ease;
    }

    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
        background: var(--navy) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--navy) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: var(--navy-2) !important;
        border-color: var(--navy-2) !important;
    }

    div[data-testid="stDownloadButton"] > button {
        background: var(--navy) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--navy) !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background: var(--navy-2) !important;
    }

    div[data-testid="stButton"] > button {
        background: #FFFFFF;
        color: var(--navy-2);
        border: 1px solid var(--border);
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #9BB0C6;
        background: #F7F9FC;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
        font-size: 13px;
        border: none;
    }

    hr {
        border: none;
        border-top: 1px solid #E5EAF0;
        margin: 2rem 0;
    }

    [data-testid="stCaptionContainer"] {
        color: #7A889A;
        font-size: 12px;
        line-height: 1.6;
    }

    .stCheckbox label {
        font-size: 13px !important;
        color: var(--text) !important;
        font-weight: 500 !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #B83B3B, #D46565);
        border-radius: 4px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2.5rem;
        }
        .qi-header {
            flex-direction: column;
            align-items: flex-start;
            padding: 22px 20px;
        }
        .qi-title {
            font-size: 22px;
        }
        [data-testid="stMetricValue"] {
            font-size: 22px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. 헤더
# =========================================================
st.markdown(
    """
    <div class="qi-header">
        <div class="qi-header-left">
            <div class="qi-badge">Quality Intelligence</div>
            <div class="qi-title">AI 소프트웨어 결함 예측</div>
            <div class="qi-subtitle">코드 메트릭 기반 결함 위험도 자동 분석 · QA 우선순위 지원</div>
        </div>
        <div class="qi-header-right">
            <div class="qi-status">
                <div class="qi-status-dot"></div>
                System Online
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. 기본 설정 · 캐시 · 공통 함수
# =========================================================
MODEL_PATH = Path(__file__).resolve().parent / "rf_model.pkl"
SCREEN_PREVIEW_LIMIT = 100
PDF_DETAIL_LIMIT = 50
PDF_PRIORITY_LIMIT = 15


@st.cache_resource
def load_model(model_path, modified_time, file_size):
    return joblib.load(model_path)


@st.cache_data(show_spinner=False)
def read_excel_cached(file_bytes):
    return pd.read_excel(io.BytesIO(file_bytes))


def dataframe_fingerprint(df):
    digest = hashlib.sha256()
    digest.update(pd.util.hash_pandas_object(df, index=True).values.tobytes())
    digest.update(repr(tuple(df.columns)).encode("utf-8"))
    digest.update(repr(tuple(map(str, df.dtypes))).encode("utf-8"))
    return digest.hexdigest()


@st.cache_data(show_spinner="모델이 데이터를 분석하고 있습니다...")
def predict_cached(model_path, modified_time, file_size, input_fingerprint, _X_pred):
    model = load_model(model_path, modified_time, file_size)
    return model.predict(_X_pred)


def format_value(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        number = float(value)
        if number.is_integer():
            return str(int(number))
        return f"{number:.3f}".rstrip("0").rstrip(".")
    return str(value)


def find_module_id_column(df):
    candidates = [
        "module_name", "module", "filename", "file_name",
        "file", "name", "id", "path", "project_source",
    ]
    return next((col for col in candidates if col in df.columns), None)


def render_html_table(df, height=490):
    preview = df.head(SCREEN_PREVIEW_LIMIT).copy()
    preview = preview.astype(object).where(pd.notna(preview), "")

    table_html = preview.to_html(
        index=False, escape=True, border=0, classes="report-table"
    )

    document = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{
                margin: 0; padding: 0;
                background: #FFFFFF;
                color: #1E2A3A;
                font-family: Inter, Arial, sans-serif;
                font-size: 12.5px;
            }}
            .table-wrap {{
                max-height: 455px;
                width: 100%;
                overflow: auto;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
            }}
            .report-table {{
                border-collapse: separate;
                border-spacing: 0;
                width: max-content;
                min-width: 100%;
                white-space: nowrap;
            }}
            .report-table th {{
                position: sticky; top: 0; z-index: 2;
                background: #F1F5F9;
                color: #334155;
                font-weight: 700;
                border-bottom: 1px solid #E2E8F0;
                font-size: 11.5px;
            }}
            .report-table th, .report-table td {{
                padding: 11px 14px;
                border-right: 1px solid #F1F5F9;
                border-bottom: 1px solid #F1F5F9;
                text-align: left;
            }}
            .report-table tbody tr:nth-child(even) td {{ background: #FAFBFC; }}
            .report-table tbody tr:hover td {{ background: #F0F7FF; }}
        </style>
    </head>
    <body>
        <div class="table-wrap">{table_html}</div>
    </body>
    </html>
    """
    components.html(document, height=height, scrolling=True)


# =========================================================
# 5. 한국어 PDF 폰트
# =========================================================
def register_korean_font():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_name = "ReportKorean"
    if font_name in pdfmetrics.getRegisteredFontNames():
        return font_name

    candidates = [
        Path(__file__).resolve().parent / "fonts" / "NanumGothic.ttf",
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    ]

    for font_path in candidates:
        if not font_path.exists():
            continue
        try:
            if font_path.suffix.lower() == ".ttc":
                font = TTFont(font_name, str(font_path), subfontIndex=0)
            else:
                font = TTFont(font_name, str(font_path))
            pdfmetrics.registerFont(font)
            return font_name
        except Exception:
            continue

    raise FileNotFoundError(
        "PDF에 사용할 한국어 폰트를 찾지 못했습니다. "
        "Windows에서는 C:/Windows/Fonts/malgun.ttf를 확인하세요."
    )


# =========================================================
# 6. 기업용 PDF 보고서 (재설계)
# =========================================================
def build_pdf_report(df_result, source_filename):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        LongTable, PageBreak, HRFlowable,
    )
    from reportlab.graphics.shapes import Drawing, Rect, String

    font_name = register_korean_font()
    buffer = io.BytesIO()
    page_size = landscape(A4)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=13 * mm,
        bottomMargin=16 * mm,
        title="AI 소프트웨어 결함 예측 분석 보고서",
        author="Quality Intelligence",
    )

    page_width = page_size[0] - doc.leftMargin - doc.rightMargin

    navy     = colors.HexColor("#0F1C2E")
    navy2    = colors.HexColor("#1A2F4A")
    blue     = colors.HexColor("#2B5A8A")
    blue_lt  = colors.HexColor("#E8F0F8")
    red      = colors.HexColor("#B83B3B")
    red_lt   = colors.HexColor("#FCEAEA")
    green    = colors.HexColor("#1F7A5A")
    green_lt = colors.HexColor("#E6F5EF")
    light    = colors.HexColor("#F4F6F9")
    border   = colors.HexColor("#E2E8F0")
    muted    = colors.HexColor("#5B6B7C")
    ink      = colors.HexColor("#1E2A3A")
    white    = colors.white

    styles = getSampleStyleSheet()

    brand = ParagraphStyle(
        "Brand", parent=styles["Normal"], fontName=font_name,
        fontSize=8, leading=11, alignment=1, textColor=blue, spaceAfter=1,
    )
    title = ParagraphStyle(
        "TitleMain", parent=styles["Title"], fontName=font_name,
        fontSize=19, leading=24, alignment=1, textColor=navy, spaceAfter=3,
    )
    subtitle = ParagraphStyle(
        "Sub", parent=styles["Normal"], fontName=font_name,
        fontSize=8.2, leading=11, alignment=1, textColor=muted, spaceAfter=2,
    )
    h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontName=font_name,
        fontSize=12, leading=16, textColor=navy, spaceBefore=6, spaceAfter=5,
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontName=font_name,
        fontSize=10, leading=13, textColor=navy2, spaceBefore=5, spaceAfter=3,
    )
    body = ParagraphStyle(
        "Body", parent=styles["Normal"], fontName=font_name,
        fontSize=8, leading=12, textColor=ink, wordWrap="CJK",
    )
    note = ParagraphStyle(
        "Note", parent=body, fontSize=6.8, leading=9.5, textColor=muted,
    )
    kpi_l = ParagraphStyle(
        "KpiL", parent=body, fontSize=7, leading=9, alignment=1, textColor=muted,
    )
    kpi_v = ParagraphStyle(
        "KpiV", parent=body, fontSize=15, leading=19, alignment=1, textColor=navy,
    )
    kpi_s = ParagraphStyle(
        "KpiS", parent=body, fontSize=6.5, leading=8.5, alignment=1, textColor=muted,
    )
    th = ParagraphStyle(
        "TH", fontName=font_name, fontSize=6.8, leading=8.5,
        textColor=white, alignment=1, wordWrap="CJK",
    )
    td = ParagraphStyle(
        "TD", fontName=font_name, fontSize=6.6, leading=8.5,
        textColor=ink, wordWrap="CJK",
    )

    # ----- 데이터 -----
    df = df_result.copy()
    if "Predicted_Defect" not in df.columns:
        raise ValueError("Predicted_Defect 컬럼이 없습니다.")

    prediction = pd.to_numeric(df["Predicted_Defect"], errors="coerce")
    if prediction.isna().any():
        raise ValueError("Predicted_Defect에 유효하지 않은 값이 있습니다.")
    if not set(prediction.unique().tolist()).issubset({0, 1}):
        raise ValueError("Predicted_Defect는 0 또는 1이어야 합니다.")

    df["Predicted_Defect"] = prediction.astype(int)
    total = len(df)
    defects = int((df["Predicted_Defect"] == 1).sum())
    normal = total - defects
    defect_rate = defects / total * 100 if total else 0.0
    normal_rate = normal / total * 100 if total else 0.0
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    id_col = find_module_id_column(df)

    excluded_cols = {
        "Predicted_Defect", "QA_Action", "defects", "actual_defect",
        "actual_label", "ground_truth", "true_label", "is_defective",
        "label", "y_true",
    }
    metric_cols = [
        col for col in df.columns
        if (col not in excluded_cols and col != id_col
            and pd.api.types.is_numeric_dtype(df[col]))
    ][:5]

    # 위험 수준 문구
    if defect_rate >= 30:
        risk_level = "높음"
        risk_color = red
        risk_comment = (
            "결함 의심 비율이 30% 이상으로, 해당 배치에 대한 집중 테스트 계획이 필요합니다. "
            "우선순위 모듈부터 코드 리뷰와 핵심 경로 테스트를 즉시 진행하는 것을 권장합니다."
        )
    elif defect_rate >= 15:
        risk_level = "중간"
        risk_color = blue
        risk_comment = (
            "결함 의심 비율이 15~30% 구간입니다. "
            "결함 의심 모듈을 1차 검토 대상으로 지정하고, 일정 내 단계적 검증을 권장합니다."
        )
    else:
        risk_level = "낮음"
        risk_color = green
        risk_comment = (
            "결함 의심 비율이 15% 미만입니다. "
            "다만 모델이 모든 실제 결함을 보장하지 않으므로 핵심 기능 회귀 테스트는 유지해야 합니다."
        )

    story = []

    # =====================================================
    # PAGE 1 — Executive Summary
    # =====================================================
    story.append(Paragraph("QUALITY INTELLIGENCE", brand))
    story.append(Spacer(1, 1.2 * mm))
    story.append(Paragraph("소프트웨어 결함 예측 분석 보고서", title))
    story.append(Paragraph(
        "Predictive Quality Assurance  ·  Risk-Based Test Prioritization  ·  Executive Summary",
        subtitle,
    ))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=navy, spaceBefore=2, spaceAfter=4,
    ))

    # 메타 정보
    meta = Table(
        [[
            Paragraph(f"<b>입력 파일</b><br/>{html.escape(str(source_filename))}", body),
            Paragraph(f"<b>분석 대상</b><br/>{total:,}개 모듈", body),
            Paragraph(f"<b>생성 일시</b><br/>{now_text}", body),
            Paragraph("<b>분석 모델</b><br/>Random Forest Classifier", body),
        ]],
        colWidths=[page_width * 0.34, page_width * 0.20, page_width * 0.23, page_width * 0.23],
    )
    meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), light),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, border),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([meta, Spacer(1, 4.5 * mm)])

    # KPI
    story.append(Paragraph("1. 핵심 예측 지표 (Key Performance Indicators)", h1))

    kpis = Table(
        [
            [
                Paragraph("전체 분석 모듈", kpi_l),
                Paragraph("결함 의심 모듈", kpi_l),
                Paragraph("정상 예측 모듈", kpi_l),
                Paragraph("결함 의심 비율", kpi_l),
            ],
            [
                Paragraph(f"{total:,}", kpi_v),
                Paragraph(f"{defects:,}", kpi_v),
                Paragraph(f"{normal:,}", kpi_v),
                Paragraph(f"{defect_rate:.1f}%", kpi_v),
            ],
            [
                Paragraph("Total Modules", kpi_s),
                Paragraph("Predicted Defect", kpi_s),
                Paragraph("Predicted Normal", kpi_s),
                Paragraph("Defect Risk Rate", kpi_s),
            ],
        ],
        colWidths=[page_width / 4] * 4,
        rowHeights=[15, 26, 13],
    )
    kpis.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, border),
        ("LINEABOVE", (0, 0), (0, 0), 2.5, blue),
        ("LINEABOVE", (1, 0), (1, 0), 2.5, red),
        ("LINEABOVE", (2, 0), (2, 0), 2.5, green),
        ("LINEABOVE", (3, 0), (3, 0), 2.5, blue),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.extend([kpis, Spacer(1, 4 * mm)])

    # 분포 차트
    story.append(Paragraph("2. 예측 결과 분포", h1))

    chart = Drawing(page_width, 52)
    label_w, value_w = 85, 125
    bar_x = label_w
    bar_w = page_width - label_w - value_w - 6

    for name, count, rate, fill, y in [
        ("결함 의심", defects, defect_rate, red, 30),
        ("정상 예측", normal, normal_rate, green, 6),
    ]:
        chart.add(String(0, y + 2, name, fontName=font_name, fontSize=8, fillColor=ink))
        chart.add(Rect(bar_x, y, bar_w, 13, fillColor=light, strokeColor=None, rx=2, ry=2))
        if rate > 0:
            chart.add(Rect(
                bar_x, y, max(bar_w * rate / 100, 2), 13,
                fillColor=fill, strokeColor=None, rx=2, ry=2,
            ))
        chart.add(String(
            bar_x + bar_w + 7, y + 2,
            f"{count:,}개  ({rate:.1f}%)",
            fontName=font_name, fontSize=7.5, fillColor=ink,
        ))
    story.extend([chart, Spacer(1, 3 * mm)])

    # 위험 수준 + 인사이트
    story.append(Paragraph("3. 위험 수준 평가 및 분석 인사이트", h1))

    risk_header = Table(
        [[
            Paragraph(f"<b>종합 위험 수준</b>", body),
            Paragraph(f"<b>{risk_level}</b>  (결함 의심 비율 {defect_rate:.1f}%)", body),
        ]],
        colWidths=[page_width * 0.28, page_width * 0.72],
    )
    risk_header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), light),
        ("BACKGROUND", (1, 0), (1, 0), white),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LINEBEFORE", (1, 0), (1, 0), 3, risk_color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([risk_header, Spacer(1, 2.5 * mm)])

    insight_text = (
        f"전체 <b>{total:,}개</b> 모듈 중 <b>{defects:,}개 ({defect_rate:.1f}%)</b>가 "
        "결함 위험 클래스로 분류되었습니다. "
        f"{risk_comment} "
        "본 결과는 Random Forest 기반 이진 분류 예측이며, 실제 결함 여부를 확정하는 근거가 아닙니다. "
        "QA 의사결정 시 보조 지표로 활용하시기 바랍니다."
    )
    insight_box = Table(
        [[Paragraph(insight_text, body)]],
        colWidths=[page_width],
    )
    insight_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), blue_lt),
        ("BOX", (0, 0), (-1, -1), 0.6, border),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, blue),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.extend([insight_box, Spacer(1, 2.5 * mm)])
    story.append(Paragraph(
        "※ 결함 의심 비율 = (모델이 결함으로 예측한 모듈 수) ÷ (전체 모듈 수). "
        "실제 결함 발생률 또는 모델 Accuracy/F1과 다른 지표입니다.",
        note,
    ))

    # =====================================================
    # PAGE 2 — QA 우선 검토
    # =====================================================
    story.append(PageBreak())
    story.append(Paragraph("QUALITY INTELLIGENCE", brand))
    story.append(Paragraph("QA 우선 검토 대상", title))
    story.append(Paragraph(
        "결함 위험 클래스 모듈 집중 테스트 권장 목록  ·  Test Prioritization",
        subtitle,
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=navy, spaceBefore=2, spaceAfter=5))

    story.append(Paragraph("4. 집중 테스트 권장 목록", h1))
    story.append(Paragraph(
        f"결함 위험으로 예측된 모듈 중 상위 <b>{min(defects, PDF_PRIORITY_LIMIT)}개</b>를 표시합니다. "
        "모듈 식별자, 주요 코드 메트릭, 권장 조치를 함께 제공합니다. "
        "실제 결함 확률 순위가 아닌, 결함 클래스로 분류된 모듈 목록입니다.",
        body,
    ))
    story.append(Spacer(1, 2.5 * mm))

    risk_rows = df.loc[df["Predicted_Defect"] == 1].head(PDF_PRIORITY_LIMIT).copy()

    if risk_rows.empty:
        empty = Table(
            [[Paragraph(
                "결함 위험 클래스로 분류된 모듈이 없습니다. "
                "기본 테스트 및 회귀 테스트 계획을 유지하시기 바랍니다.",
                body,
            )]],
            colWidths=[page_width],
        )
        empty.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), green_lt),
            ("BOX", (0, 0), (-1, -1), 0.6, border),
            ("LINEBEFORE", (0, 0), (0, -1), 3.5, green),
            ("LEFTPADDING", (0, 0), (-1, -1), 11),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        story.append(empty)
    else:
        headers = ["No", "모듈 식별자"] + [str(c) for c in metric_cols] + ["권장 조치"]
        pdata = [[Paragraph(html.escape(h), th) for h in headers]]

        for i, (_, row) in enumerate(risk_rows.iterrows(), start=1):
            ident = (
                str(row[id_col]) if id_col and pd.notna(row[id_col])
                else f"모듈-{i:03d}"
            )
            vals = [str(i), ident] + [format_value(row[c]) for c in metric_cols] + ["집중 테스트 / 코드 리뷰"]
            pdata.append([Paragraph(html.escape(str(v)), td) for v in vals])

        weights = [0.5, 2.2] + [1.0] * len(metric_cols) + [2.2]
        wsum = sum(weights)
        widths = [page_width * w / wsum for w in weights]

        ptable = Table(pdata, colWidths=widths, repeatRows=1)
        ptable.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("GRID", (0, 0), (-1, -1), 0.35, border),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, light]),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ]))
        story.append(ptable)

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("5. 권장 QA 프로세스", h1))

    process_items = [
        ("01", "우선순위 지정", "본 보고서의 결함 의심 모듈을 1차 검토 대상으로 등록합니다."),
        ("02", "코드 리뷰", "복잡도·규모 지표가 높은 모듈부터 변경 이력과 함께 리뷰합니다."),
        ("03", "테스트 설계", "핵심 기능, 경계 조건, 예외 경로를 중심으로 테스트 케이스를 보강합니다."),
        ("04", "실행 및 기록", "테스트 결과를 기록하고, 실제 결함 발견 여부를 모델 예측과 대조합니다."),
        ("05", "피드백", "오탐/미탐 사례를 정리하여 향후 모델 개선 및 품질 지표 고도화에 활용합니다."),
    ]

    proc_data = [[
        Paragraph("<b>단계</b>", th),
        Paragraph("<b>활동</b>", th),
        Paragraph("<b>상세 내용</b>", th),
    ]]
    for num, act, detail in process_items:
        proc_data.append([
            Paragraph(num, td),
            Paragraph(act, td),
            Paragraph(detail, td),
        ])

    proc_table = Table(proc_data, colWidths=[page_width * 0.10, page_width * 0.18, page_width * 0.72])
    proc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy2),
        ("GRID", (0, 0), (-1, -1), 0.35, border),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, light]),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ]))
    story.append(proc_table)
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "참고: 현재 모델은 예측 확률(probability)을 저장하지 않으므로, "
        "위 목록은 결함 클래스(1)로 분류된 모듈을 나열한 것이며 위험도 순위가 아닙니다.",
        note,
    ))

    # =====================================================
    # PAGE 3 — 세부 표본
    # =====================================================
    story.append(PageBreak())
    story.append(Paragraph("QUALITY INTELLIGENCE", brand))
    story.append(Paragraph("세부 예측 리포트", title))
    story.append(Paragraph(
        f"전체 {total:,}개 모듈 중 결함 위험 우선 표본 최대 {PDF_DETAIL_LIMIT}개  ·  Detailed Sample",
        subtitle,
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=navy, spaceBefore=2, spaceAfter=4))

    sample = df.sort_values("Predicted_Defect", ascending=False, kind="stable").head(PDF_DETAIL_LIMIT).copy()
    story.append(Paragraph(
        f"요약 통계는 <b>전체 {total:,}개</b> 기준이며, "
        f"아래 표는 결함 위험 모듈을 우선 포함한 <b>{len(sample):,}개</b> 표본입니다.",
        body,
    ))
    story.append(Spacer(1, 2.5 * mm))

    detail_cols = []
    if id_col is not None:
        detail_cols.append(id_col)
    detail_cols.extend(metric_cols)
    detail_cols.extend(["Predicted_Defect", "QA_Action"])
    detail_cols = list(dict.fromkeys(c for c in detail_cols if c in sample.columns))

    sample_table = sample[detail_cols].copy()

    tdata = [[Paragraph(html.escape(str(c)), th) for c in sample_table.columns]]
    for _, row in sample_table.iterrows():
        vals = []
        for col in sample_table.columns:
            val = row[col]
            if col == "QA_Action":
                val = (
                    "결함 위험 · 집중 테스트"
                    if row["Predicted_Defect"] == 1
                    else "정상 예측 · 일반 테스트"
                )
            elif col == "Predicted_Defect":
                val = "1 (위험)" if int(row[col]) == 1 else "0 (정상)"
            vals.append(Paragraph(html.escape(format_value(val)), td))
        tdata.append(vals)

    weights = []
    for col in sample_table.columns:
        if col == id_col:
            weights.append(2.2)
        elif col == "QA_Action":
            weights.append(2.3)
        elif col == "Predicted_Defect":
            weights.append(1.3)
        else:
            weights.append(1.0)
    wsum = sum(weights)
    dwidths = [page_width * w / wsum for w in weights]

    dtable = LongTable(tdata, colWidths=dwidths, repeatRows=1, splitByRow=1)
    dtable.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("GRID", (0, 0), (-1, -1), 0.3, border),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, light]),
    ]))
    story.append(dtable)

    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=border, spaceBefore=2, spaceAfter=3))
    story.append(Paragraph(
        "본 보고서는 Quality Intelligence 시스템의 AI 결함 예측 결과를 기반으로 자동 생성되었습니다. "
        "의사결정 시 현업 QA 기준 및 프로젝트 특성을 함께 고려하시기 바랍니다.",
        note,
    ))

    # 푸터
    def draw_page(canvas, current_doc):
        canvas.saveState()
        canvas.setStrokeColor(border)
        canvas.setLineWidth(0.6)
        canvas.line(
            current_doc.leftMargin, 12 * mm,
            page_size[0] - current_doc.rightMargin, 12 * mm,
        )
        canvas.setFont(font_name, 6.5)
        canvas.setFillColor(muted)
        canvas.drawString(
            current_doc.leftMargin, 7 * mm,
            "QUALITY INTELLIGENCE  |  AI Software Defect Prediction Report  |  Confidential",
        )
        canvas.drawRightString(
            page_size[0] - current_doc.rightMargin, 7 * mm,
            f"{current_doc.page}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    return buffer.getvalue()


def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {MODEL_PATH}")
    stat = MODEL_PATH.stat()
    model = load_model(str(MODEL_PATH), stat.st_mtime_ns, stat.st_size)
    return model, stat


# =========================================================
# 7. 업로드 영역
# =========================================================
st.markdown('<div class="section-label">Data Input</div>', unsafe_allow_html=True)
st.markdown("### 분석 데이터 업로드")
st.markdown(
    '<div style="font-size:13px;color:#5B6B7C;margin-bottom:14px;line-height:1.5;">'
    "예측 결과 파일 또는 신규 모듈 메트릭 파일(.xlsx)을 업로드하세요."
    "</div>",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Excel 파일",
    type=["xlsx"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown(
        """
        <div style="
            background:#FFFFFF;
            border:1px solid #E2E8F0;
            border-radius:14px;
            padding:40px 36px;
            margin-top:8px;
            box-shadow: 0 1px 3px rgba(15,28,46,0.04), 0 4px 16px rgba(15,28,46,0.05);
        ">
            <div style="
                display:inline-block;
                background:#E8F0F8;
                color:#2B5A8A;
                font-size:11px;
                font-weight:700;
                letter-spacing:1px;
                padding:5px 12px;
                border-radius:20px;
                margin-bottom:14px;
            ">READY</div>
            <div style="
                color:#0F1C2E;
                font-size:20px;
                font-weight:700;
                letter-spacing:-0.4px;
                margin-bottom:10px;
            ">분석을 시작할 준비가 되었습니다</div>
            <div style="
                color:#5B6B7C;
                font-size:13.5px;
                line-height:1.75;
                max-width:560px;
            ">
                Excel 파일을 업로드하면 결함 예측 결과, 모듈별 리포트,
                QA 권장 조치 및 PDF 보고서를 확인할 수 있습니다.<br/>
                기존 예측 결과 파일에는 <b>Predicted_Defect</b> 컬럼이 필요합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# =========================================================
# 8. 데이터 처리 및 예측
# =========================================================
try:
    file_bytes = uploaded_file.getvalue()
    df_raw = read_excel_cached(file_bytes)

    if df_raw.empty:
        st.error("업로드한 Excel 파일에 데이터가 없습니다.")
        st.stop()

    df_raw.columns = df_raw.columns.astype(str).str.strip()
    duplicates = df_raw.columns[df_raw.columns.duplicated()].tolist()
    if duplicates:
        st.error("중복된 컬럼명이 있습니다: " + ", ".join(duplicates))
        st.stop()

    if "Predicted_Defect" in df_raw.columns:
        predictions = pd.to_numeric(df_raw["Predicted_Defect"], errors="coerce")
        if predictions.isna().any():
            st.error("Predicted_Defect 컬럼에 유효하지 않은 값이 있습니다.")
            st.stop()
        if not set(predictions.unique().tolist()).issubset({0, 1}):
            st.error("Predicted_Defect 값은 0 또는 1이어야 합니다.")
            st.stop()

        df_result = df_raw.copy()
        df_result["Predicted_Defect"] = predictions.astype(int).to_numpy()
        df_result["QA_Action"] = [
            "결함 위험 - 집중 테스트" if v == 1 else "정상 예측 - 일반 테스트"
            for v in df_result["Predicted_Defect"]
        ]
        data_mode = "기존 예측 결과"

    else:
        try:
            model, model_stat = get_model()
        except Exception as e:
            st.error(f"모델 로드 실패: {e}")
            st.stop()

        exclude_cols = [
            "Predicted_Defect", "QA_Action", "defects",
            "project_source", "id",
        ]

        expected_features = getattr(model, "feature_names_in_", None)

        if expected_features is not None:
            expected_features = [str(c).strip() for c in expected_features]
            missing_cols = [c for c in expected_features if c not in df_raw.columns]
            if missing_cols:
                st.error("모델에 필요한 입력 컬럼이 없습니다:\n" + ", ".join(missing_cols))
                st.stop()
            X_pred = df_raw.loc[:, expected_features].copy()
        else:
            X_pred = df_raw.drop(
                columns=[c for c in exclude_cols if c in df_raw.columns],
                errors="ignore",
            )
            expected_count = getattr(model, "n_features_in_", None)
            if expected_count is not None and X_pred.shape[1] != expected_count:
                st.error(
                    f"모델 입력 컬럼 수: {expected_count}개 / "
                    f"현재 입력 컬럼 수: {X_pred.shape[1]}개"
                )
                st.stop()

        if X_pred.shape[1] == 0:
            st.error("예측에 사용할 컬럼이 없습니다.")
            st.stop()

        invalid_cols = []
        for col in X_pred.columns:
            if not pd.api.types.is_numeric_dtype(X_pred[col]):
                converted = pd.to_numeric(X_pred[col], errors="coerce")
                if (X_pred[col].notna() & converted.isna()).any():
                    invalid_cols.append(col)
                else:
                    X_pred[col] = converted

        if invalid_cols:
            st.error("숫자로 변환할 수 없는 입력 컬럼: " + ", ".join(invalid_cols))
            st.stop()

        if X_pred.isna().any().any():
            st.error("예측 입력에 결측값이 있습니다. Excel 파일을 수정한 후 다시 업로드하세요.")
            st.stop()

        predictions = predict_cached(
            str(MODEL_PATH),
            model_stat.st_mtime_ns,
            model_stat.st_size,
            dataframe_fingerprint(X_pred),
            X_pred,
        )
        predictions = pd.to_numeric(pd.Series(predictions), errors="coerce")

        if predictions.isna().any():
            st.error("모델 예측 결과에 유효하지 않은 값이 있습니다.")
            st.stop()
        if not set(predictions.unique().tolist()).issubset({0, 1}):
            st.error("모델 출력은 0/1 이진 분류여야 합니다.")
            st.stop()
        if len(predictions) != len(df_raw):
            st.error("예측 결과 행 수가 원본 데이터와 다릅니다.")
            st.stop()

        df_result = df_raw.copy()
        df_result["Predicted_Defect"] = predictions.astype(int).to_numpy()
        df_result["QA_Action"] = [
            "결함 위험 - 집중 테스트" if v == 1 else "정상 예측 - 일반 테스트"
            for v in df_result["Predicted_Defect"]
        ]
        data_mode = "신규 데이터 예측"

    total_count = len(df_result)
    defect_count = int((df_result["Predicted_Defect"] == 1).sum())
    normal_count = total_count - defect_count
    defect_rate = defect_count / total_count * 100 if total_count else 0.0
    normal_rate = normal_count / total_count * 100 if total_count else 0.0

    st.markdown(
        f"""
        <div style="
            display:flex; flex-wrap:wrap; align-items:center; gap:10px;
            margin: 4px 0 22px 0; color:#5B6B7C; font-size:12px;
        ">
            <span style="
                background:#E6F5EF; color:#1F7A5A;
                padding:5px 11px; border-radius:6px; font-weight:650;
            ">READY</span>
            <span>{html.escape(uploaded_file.name)}</span>
            <span style="color:#CBD5E1;">·</span>
            <span>{data_mode}</span>
            <span style="color:#CBD5E1;">·</span>
            <span>{total_count:,}개 모듈</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # 9. 예측 결과 요약
    # =====================================================
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    st.subheader("예측 결과 요약")
    st.markdown(
        '<div style="font-size:13px;color:#5B6B7C;margin-bottom:16px;">'
        "전체 분석 결과를 기준으로 집계한 핵심 지표입니다."
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("전체 검사 모듈", f"{total_count:,}개")
    c2.metric("결함 의심 모듈", f"{defect_count:,}개")
    c3.metric("정상 예측 모듈", f"{normal_count:,}개")
    c4.metric("결함 의심 비율", f"{defect_rate:.1f}%")

    # =====================================================
    # 10. 세부 리포트
    # =====================================================
    st.divider()
    st.markdown('<div class="section-label">Module Inspection</div>', unsafe_allow_html=True)
    st.subheader("세부 예측 리포트")
    st.markdown(
        f'<div style="font-size:13px;color:#5B6B7C;margin-bottom:14px;">'
        f"전체 {total_count:,}개 모듈 중 최대 "
        f"{min(total_count, SCREEN_PREVIEW_LIMIT):,}개를 표시합니다."
        f"</div>",
        unsafe_allow_html=True,
    )

    risk_only = st.checkbox("결함 의심 모듈만 보기", value=False)
    df_table = (
        df_result.loc[df_result["Predicted_Defect"] == 1]
        if risk_only else df_result
    )
    render_html_table(df_table)
    st.caption(
        f"현재 필터 대상: {len(df_table):,}개 · "
        f"화면 표시: {min(len(df_table), SCREEN_PREVIEW_LIMIT):,}개"
    )

    # =====================================================
    # 11. 상세 분석
    # =====================================================
    st.divider()
    st.markdown('<div class="section-label">QA Analytics</div>', unsafe_allow_html=True)
    st.subheader("결함 예측 상세 분석")

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("결함 의심 모듈", f"{defect_count:,}개")
    a2.metric("결함 의심 비율", f"{defect_rate:.1f}%")
    a3.metric("정상 예측 모듈", f"{normal_count:,}개")
    a4.metric("정상 예측 비율", f"{normal_rate:.1f}%")

    st.markdown("#### 결함 위험 분포")
    st.write(
        f"전체 {total_count:,}개 모듈 중 "
        f"{defect_count:,}개가 결함 위험 클래스로 예측되었습니다."
    )
    st.progress(min(max(defect_rate / 100, 0.0), 1.0))

    chart_html = f"""
    <!DOCTYPE html>
    <html lang="ko"><head><meta charset="UTF-8">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0; padding: 18px 20px;
            background: #FFFFFF; color: #1E2A3A;
            font-family: Inter, Arial, sans-serif; font-size: 13px;
        }}
        .panel {{ padding: 8px 4px; }}
        .row {{
            display: grid;
            grid-template-columns: 110px minmax(80px, 1fr) 150px;
            gap: 14px; align-items: center; margin: 18px 0;
        }}
        .label {{ color: #334155; font-weight: 600; }}
        .track {{
            height: 14px; background: #EDF1F5;
            border-radius: 6px; overflow: hidden;
        }}
        .fill {{ height: 100%; border-radius: 6px; }}
        .defect {{ background: linear-gradient(90deg, #B83B3B, #D46565); }}
        .normal {{ background: linear-gradient(90deg, #1F7A5A, #34A87A); }}
        .value {{
            text-align: right; white-space: nowrap;
            color: #5B6B7C; font-variant-numeric: tabular-nums;
            font-size: 12.5px;
        }}
    </style></head>
    <body>
        <div class="panel">
            <div class="row">
                <div class="label">결함 의심</div>
                <div class="track"><div class="fill defect" style="width:{defect_rate:.2f}%"></div></div>
                <div class="value">{defect_count:,}개 · {defect_rate:.1f}%</div>
            </div>
            <div class="row">
                <div class="label">정상 예측</div>
                <div class="track"><div class="fill normal" style="width:{normal_rate:.2f}%"></div></div>
                <div class="value">{normal_count:,}개 · {normal_rate:.1f}%</div>
            </div>
        </div>
    </body></html>
    """
    components.html(chart_html, height=140, scrolling=False)

    st.subheader("QA 권장 조치")
    if defect_count > 0:
        st.warning(
            f"결함 위험으로 분류된 **{defect_count:,}개** 모듈을 우선 검토 대상으로 지정하고, "
            "코드 리뷰와 주요 기능 테스트를 먼저 수행하는 것을 권장합니다."
        )
    else:
        st.success(
            "결함 위험으로 분류된 모듈이 없습니다. "
            "기본 테스트와 회귀 테스트는 유지하세요."
        )
    st.caption(
        "결함 의심 비율은 실제 결함률이 아니라 "
        "모델이 결함 클래스로 예측한 모듈의 비율입니다."
    )

    # =====================================================
    # 12. PDF 보고서
    # =====================================================
    st.divider()
    st.markdown('<div class="section-label">Report Export</div>', unsafe_allow_html=True)
    st.subheader("최종 PDF 보고서")
    st.markdown(
        f'<div style="font-size:13px;color:#5B6B7C;margin-bottom:14px;">'
        f"Executive Summary, 위험 수준 평가, QA 우선 검토 목록, "
        f"권장 프로세스, 세부 표본 최대 {PDF_DETAIL_LIMIT}개를 포함합니다."
        f"</div>",
        unsafe_allow_html=True,
    )

    try:
        import reportlab  # noqa: F401
        reportlab_available = True
    except ImportError:
        reportlab_available = False

    if not reportlab_available:
        st.error("PDF 생성 라이브러리가 설치되어 있지 않습니다.")
        st.code("python -m pip install reportlab", language="bash")
    else:
        report_key = hashlib.sha256(
            (uploaded_file.name + dataframe_fingerprint(df_result)).encode("utf-8")
        ).hexdigest()

        if st.session_state.get("pdf_report_key") != report_key:
            st.session_state["pdf_report_key"] = report_key
            st.session_state["pdf_report_bytes"] = None
            st.session_state["pdf_report_filename"] = None

        if st.button("PDF 보고서 생성", type="primary", key="create_pdf_report"):
            try:
                with st.spinner("기업용 분석 보고서를 생성하고 있습니다..."):
                    pdf_bytes = build_pdf_report(df_result, uploaded_file.name)
                st.session_state["pdf_report_bytes"] = pdf_bytes
                st.session_state["pdf_report_filename"] = (
                    "AI_결함예측_분석보고서_"
                    + datetime.now().strftime("%Y%m%d_%H%M")
                    + ".pdf"
                )
                st.session_state["pdf_report_key"] = report_key
            except Exception as e:
                st.error(
                    f"PDF 생성에 실패했습니다.\n\n"
                    f"오류 유형: {type(e).__name__}\n\n상세 내용: {e}"
                )

        if (
            st.session_state.get("pdf_report_key") == report_key
            and st.session_state.get("pdf_report_bytes")
        ):
            st.success("PDF 보고서 생성 완료")
            st.download_button(
                label="PDF 보고서 다운로드",
                data=st.session_state["pdf_report_bytes"],
                file_name=st.session_state["pdf_report_filename"],
                mime="application/pdf",
                key="download_pdf_report",
            )

except Exception as e:
    st.error(
        "데이터 처리 중 오류가 발생했습니다.\n\n"
        f"오류 유형: {type(e).__name__}\n\n상세 내용: {e}"
    )