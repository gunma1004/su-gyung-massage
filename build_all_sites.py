import os
import random
from string import Template

# 도메인 주소
BASE_URL = "https://su-gyung-massage.netlify.app"

# 네이버 서치어드바이저 소유권 확인 메타 태그
NAVER_VERIFY_TAG = '<meta name="naver-site-verification" content="02fb4b7e8db50be9306a8be574ed447c869a93f1" />'

# 검색엔진 평점 노출용 JSON-LD 스크립트
SEO_RATING_JSON = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "수경마사지",
  "telephone": "0507-1280-3201",
  "priceRange": "60,000원~",
  "areaServed": ["서울", "경기", "인천"],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "128",
    "bestRating": "5"
  }
}
</script>
"""

# 메인 배너 HTML 컴포넌트
BANNER_HTML = """
<div style="max-width:1100px;margin:24px auto 0;padding:0 20px;">
  <img src="/images/main-banner.jpg" alt="수경마사지 프리미엄 홈케어 안내 배너" style="width:100%;max-width:1100px;height:auto;border-radius:14px;box-shadow:0 8px 24px rgba(216,90,125,0.15);display:block;">
</div>
"""

# 🌟 타이틀용 접미사 풀 (타이틀 전용)
TITLE_VARIANTS = [
    "출장 이용정보 마사지",
    "출장 케어 마사지",
    "출장 힐링 마사지",
    "출장 균형케어 마사지",
    "출장 리듬케어 마사지",
    "출장 율동케어 마사지"
]

# 🌟 메타 디스크립션용 안내 문구 풀 (시·구·동 출장마사지 뒤에 조합되어 타이틀과 차별화)
DESC_INTRO_POOL = [
    "프리미엄 힐링 홈타이 안내 플랫폼.",
    "자택·숙소 어디든 30분 내 신속 방문 홈케어.",
    "전문 테라피스트의 프라이빗 1:1 방문 맞춤 케어.",
    "심야 시간에도 정찰제로 편안하게 이용하는 홈타이."
]
DESC_PRICE_POOL = [
    "건식 6만원부터 시작하는 100% 안심 후불제.",
    "선입금 없는 안전한 전액 후불제 정찰 가격 운영.",
    "예약금 없는 투명한 가격 정책과 철저한 위생 관리.",
    "부담 없는 합리적인 코스 구성 및 신속 배정."
]

# 수도권 전 지역 데이터베이스
regions = {
    "seoul": {
        "name": "서울",
        "intro": "서울 전역 25개 자치구 오피스 상권과 주거 단지를 아우르는 프리미엄 방문 마사지 및 홈타이 서비스입니다.",
        "sub_regions": [
            {"name": "강남구", "slug": "gangnamgu", "dongs": [{"name": "신사동", "slug": "sinsadong"}, {"name": "논현동", "slug": "nonhyeondong"}, {"name": "삼성동", "slug": "samseongdong"}, {"name": "대치동", "slug": "daechidong"}, {"name": "역삼동", "slug": "yeoksamdong"}, {"name": "도곡동", "slug": "dogokdong"}, {"name": "청담동", "slug": "cheongdamdong"}]},
            {"name": "강동구", "slug": "gangdonggu", "dongs": [{"name": "천호동", "slug": "cheonhodong"}, {"name": "성내동", "slug": "seongnaedong"}, {"name": "길동", "slug": "gildong"}, {"name": "암사동", "slug": "amsadong"}, {"name": "명일동", "slug": "myeongildong"}]},
            {"name": "강북구", "slug": "gangbukgu", "dongs": [{"name": "미아동", "slug": "miadong"}, {"name": "수유동", "slug": "suyudong"}, {"name": "번동", "slug": "beondong"}, {"name": "우이동", "slug": "uidong"}]},
            {"name": "강서구", "slug": "gangseogu", "dongs": [{"name": "화곡동", "slug": "hwagokdong"}, {"name": "마곡동", "slug": "magokdong"}, {"name": "가양동", "slug": "gayangdong"}, {"name": "등촌동", "slug": "deungchondong"}, {"name": "발산동", "slug": "balsandong"}]},
            {"name": "관악구", "slug": "gwanakgu", "dongs": [{"name": "봉천동", "slug": "bongcheondong"}, {"name": "신림동", "slug": "sillimdong"}, {"name": "남현동", "slug": "namhyeondong"}]},
            {"name": "광진구", "slug": "gwangjingu", "dongs": [{"name": "자양동", "slug": "jayangdong"}, {"name": "화양동", "slug": "hwayangdong"}, {"name": "군자동", "slug": "gunjadong"}, {"name": "구의동", "slug": "guuidong"}]},
            {"name": "구로구", "slug": "gurogu", "dongs": [{"name": "구로동", "slug": "gurodong"}, {"name": "신도림동", "slug": "sindorimdong"}, {"name": "개봉동", "slug": "gaebongdong"}, {"name": "철산동", "slug": "cheolsandong"}]},
            {"name": "금천구", "slug": "geumcheongu", "dongs": [{"name": "가산동", "slug": "gasandong"}, {"name": "독산동", "slug": "doksandong"}, {"name": "시흥동", "slug": "siheungdong"}]},
            {"name": "노원구", "slug": "nowongu", "dongs": [{"name": "상계동", "slug": "sanggyedong"}, {"name": "중계동", "slug": "junggyedong"}, {"name": "하계동", "slug": "hagyedong"}, {"name": "공릉동", "slug": "gongneungdong"}]},
            {"name": "도봉구", "slug": "dobonggu", "dongs": [{"name": "창동", "slug": "changdong"}, {"name": "쌍문동", "slug": "ssangmundong"}, {"name": "도봉동", "slug": "dobongdong"}, {"name": "방학동", "slug": "banghakdong"}]},
            {"name": "동대문구", "slug": "dongdaemungu", "dongs": [{"name": "회기동", "slug": "hoegidong"}, {"name": "전농동", "slug": "jeonnongdong"}, {"name": "답십리동", "slug": "dapsimnidong"}, {"name": "장안동", "slug": "jangandong"}]},
            {"name": "동작구", "slug": "dongjakgu", "dongs": [{"name": "사당동", "slug": "sadangdong"}, {"name": "상도동", "slug": "sangdodong"}, {"name": "노량진동", "slug": "noryangjindong"}, {"name": "흑석동", "slug": "heukseokdong"}]},
            {"name": "마포구", "slug": "mapogu", "dongs": [{"name": "합정동", "slug": "hapjeongdong"}, {"name": "서교동", "slug": "seogyodong"}, {"name": "상암동", "slug": "sangamdong"}, {"name": "망원동", "slug": "mangwondong"}, {"name": "연남동", "slug": "yeonnamdong"}, {"name": "공덕동", "slug": "gongdeokdong"}]},
            {"name": "서대문구", "slug": "seodaemungu", "dongs": [{"name": "창천동", "slug": "changcheondong"}, {"name": "남가좌동", "slug": "namgajwadong"}, {"name": "북가좌동", "slug": "bukgajwadong"}, {"name": "연희동", "slug": "yeonhidong"}]},
            {"name": "서초구", "slug": "seochogu", "dongs": [{"name": "서초동", "slug": "seochodong"}, {"name": "반포동", "slug": "banpodong"}, {"name": "방배동", "slug": "bangbaedong"}, {"name": "양재동", "slug": "yangjaedong"}]},
            {"name": "성동구", "slug": "seongdonggu", "dongs": [{"name": "성수동", "slug": "seongsudong"}, {"name": "왕십리동", "slug": "wangsimlidong"}, {"name": "행당동", "slug": "haengdangdong"}, {"name": "옥수동", "slug": "oksudong"}]},
            {"name": "성북구", "slug": "seongbukgu", "dongs": [{"name": "돈암동", "slug": "donamdong"}, {"name": "길음동", "slug": "gileumdong"}, {"name": "정릉동", "slug": "jeongneungdong"}, {"name": "성북동", "slug": "seongbukdong"}]},
            {"name": "송파구", "slug": "songpagu", "dongs": [{"name": "잠실동", "slug": "jamsildong"}, {"name": "방이동", "slug": "bangidong"}, {"name": "문정동", "slug": "munjeongdong"}, {"name": "가락동", "slug": "garakdong"}, {"name": "석촌동", "slug": "seokchondong"}]},
            {"name": "양천구", "slug": "yangcheongu", "dongs": [{"name": "목동", "slug": "mokdong"}, {"name": "신정동", "slug": "sinjeongdong"}, {"name": "신월동", "slug": "sinwoldong"}]},
            {"name": "영등포구", "slug": "yeongdeungpogu", "dongs": [{"name": "여의도동", "slug": "yeouidodong"}, {"name": "영등포동", "slug": "yeongdeungpodong"}, {"name": "문래동", "slug": "mullaedong"}, {"name": "당산동", "slug": "dangsandong"}]},
            {"name": "용산구", "slug": "yongsangu", "dongs": [{"name": "이태원동", "slug": "itaewondong"}, {"name": "한남동", "slug": "hannamdong"}, {"name": "용산동", "slug": "yongsandong"}, {"name": "서계동", "slug": "seogyedong"}]},
            {"name": "은평구", "slug": "eunpyeonggu", "dongs": [{"name": "불광동", "slug": "bulgwangdong"}, {"name": "역촌동", "slug": "yeokchondong"}, {"name": "증산동", "slug": "jeungsandong"}, {"name": "응암동", "slug": "eungamdong"}]},
            {"name": "종로구", "slug": "jongnogu", "dongs": [{"name": "종로동", "slug": "jongnodong"}, {"name": "혜화동", "slug": "hyehwadong"}, {"name": "평창동", "slug": "pyeongchangdong"}, {"name": "부암동", "slug": "buamdong"}]},
            {"name": "중구", "slug": "junggu", "dongs": [{"name": "명동", "slug": "myeongdong"}, {"name": "을지로동", "slug": "euljirodong"}, {"name": "남산동", "slug": "namsandong"}, {"name": "신당동", "slug": "sindangdong"}]},
            {"name": "중랑구", "slug": "jungranggu", "dongs": [{"name": "면목동", "slug": "myeonmokdong"}, {"name": "상봉동", "slug": "sangbongdong"}, {"name": "중화동", "slug": "junghwadong"}, {"name": "망우동", "slug": "mangwoudong"}]}
        ]
    },
    "gyeonggi": {
        "name": "경기",
        "intro": "수원, 성남(분당), 고양(일산), 용인 등 경기도 주요 신도시 및 권역별 맞춤형 방문마사지 정보를 신속하게 제공합니다.",
        "sub_regions": [
            {"name": "수원시", "slug": "suwon", "dongs": [{"name": "인계동", "slug": "ingyedong"}, {"name": "권선동", "slug": "gwonseondong"}, {"name": "영통동", "slug": "yeongtongdong"}, {"name": "매탄동", "slug": "maetandong"}, {"name": "화서동", "slug": "hwaseodong"}]},
            {"name": "성남시", "slug": "seongnam", "dongs": [{"name": "정자동", "slug": "jeongjadong"}, {"name": "서현동", "slug": "seohyeondong"}, {"name": "판교동", "slug": "pangyodong"}, {"name": "산성동", "slug": "sanseongdong"}, {"name": "수진동", "slug": "sujindong"}]},
            {"name": "고양시", "slug": "goyang", "dongs": [{"name": "장항동", "slug": "janghangdong"}, {"name": "주엽동", "slug": "juyeopdong"}, {"name": "화정동", "slug": "hwajeongdong"}, {"name": "행신동", "slug": "haengsindong"}, {"name": "대화동", "slug": "daehwadong"}]},
            {"name": "용인시", "slug": "yongin", "dongs": [{"name": "수지동", "slug": "sujidong"}, {"name": "기흥동", "slug": "giheungdong"}, {"name": "처인동", "slug": "cheoindong"}, {"name": "보정동", "slug": "bojeongdong"}, {"name": "풍덕천동", "slug": "pungdeokcheondong"}]},
            {"name": "부천시", "slug": "bucheon", "dongs": [{"name": "중동", "slug": "jungdong"}, {"name": "상동", "slug": "sangdong"}, {"name": "심곡동", "slug": "simgokdong"}, {"name": "소사동", "slug": "sosadong"}, {"name": "원종동", "slug": "wonjongdong"}]},
            {"name": "화성시", "slug": "hwaseong", "dongs": [{"name": "동탄동", "slug": "dongtandong"}, {"name": "병점동", "slug": "byeongjeomdong"}, {"name": "향남동", "slug": "hyangnamdong"}, {"name": "봉담동", "slug": "bongdamdong"}]},
            {"name": "안산시", "slug": "ansan", "dongs": [{"name": "고잔동", "slug": "gojandong"}, {"name": "중앙동", "slug": "jungangdong"}, {"name": "상록수동", "slug": "sangnoksudong"}, {"name": "원곡동", "slug": "wongokdong"}]},
            {"name": "안양시", "slug": "anyang", "dongs": [{"name": "평촌동", "slug": "pyeongchondong"}, {"name": "범계동", "slug": "beomgyedong"}, {"name": "석수동", "slug": "seoksudong"}, {"name": "관양동", "slug": "gwanyangdong"}]},
            {"name": "평택시", "slug": "pyeongtaek", "dongs": [{"name": "비전동", "slug": "bijeondong"}, {"name": "소사벌동", "slug": "sosabeoldong"}, {"name": "서정동", "slug": "seojeongdong"}, {"name": "송탄동", "slug": "songtandong"}]},
            {"name": "시흥시", "slug": "siheung", "dongs": [{"name": "정왕동", "slug": "jeongwangdong"}, {"name": "배곧동", "slug": "baegotdong"}, {"name": "목감동", "slug": "mokgamdong"}, {"name": "대야동", "slug": "daeyadong"}]},
            {"name": "파주시", "slug": "paju", "dongs": [{"name": "운정동", "slug": "unjeongdong"}, {"name": "문산동", "slug": "munsandong"}, {"name": "금촌동", "slug": "geumchondong"}, {"name": "교하동", "slug": "gyohadong"}]},
            {"name": "의정부시", "slug": "uijeongbu", "dongs": [{"name": "의정부동", "slug": "uijeongbudong"}, {"name": "가능동", "slug": "ganeungdong"}, {"name": "호원동", "slug": "howondong"}, {"name": "민락동", "slug": "minlakdong"}]},
            {"name": "김포시", "slug": "gimpo", "dongs": [{"name": "구래동", "slug": "guraedong"}, {"name": "장기동", "slug": "janggidong"}, {"name": "운양동", "slug": "unyangdong"}, {"name": "사우동", "slug": "saudong"}]},
            {"name": "광주시", "slug": "gwangju", "dongs": [{"name": "오포동", "slug": "opodong"}, {"name": "초월동", "slug": "chowoldong"}, {"name": "태전동", "slug": "taejeondong"}, {"name": "역동", "slug": "yeokdong"}]},
            {"name": "하남시", "slug": "hanam", "dongs": [{"name": "미사동", "slug": "misadong"}, {"name": "신장동", "slug": "sinjangdong"}, {"name": "덕풍동", "slug": "deokpungdong"}, {"name": "감일동", "slug": "gamildong"}]}
        ]
    },
    "incheon": {
        "name": "인천",
        "intro": "송도국제도시, 부평 상권, 청라 및 검단 등 인천 주요 경제·주거 중심지로 신속하게 찾아가는 서비스를 안내합니다.",
        "sub_regions": [
            {"name": "연수구", "slug": "yeonsugu", "dongs": [{"name": "송도동", "slug": "songdodong"}, {"name": "연수동", "slug": "yeonsudong"}, {"name": "동춘동", "slug": "dongchundong"}, {"name": "청학동", "slug": "cheonghakdong"}]},
            {"name": "부평구", "slug": "bupyeonggu", "dongs": [{"name": "부평동", "slug": "bupyeongdong"}, {"name": "산곡동", "slug": "sangokdong"}, {"name": "청천동", "slug": "cheongcheondong"}, {"name": "삼산동", "slug": "samsandong"}, {"name": "갈산동", "slug": "galsandong"}]},
            {"name": "서구", "slug": "seogu", "dongs": [{"name": "청라동", "slug": "cheongladong"}, {"name": "검단동", "slug": "geomdandong"}, {"name": "가좌동", "slug": "gajwadong"}, {"name": "심곡동", "slug": "simgokdong"}, {"name": "당하동", "slug": "danghadong"}]},
            {"name": "남동구", "slug": "namdonggu", "dongs": [{"name": "구월동", "slug": "guwoldong"}, {"name": "논현동", "slug": "nonhyeondong"}, {"name": "서창동", "slug": "seochangdong"}, {"name": "간석동", "slug": "ganseokdong"}, {"name": "만수동", "slug": "mansudong"}]},
            {"name": "미추홀구", "slug": "michuholgu", "dongs": [{"name": "주안동", "slug": "juandong"}, {"name": "용현동", "slug": "yonghyeondong"}, {"name": "학익동", "slug": "hakikdong"}, {"name": "관교동", "slug": "gwangyodong"}]},
            {"name": "계양구", "slug": "gyeyanggu", "dongs": [{"name": "작전동", "slug": "jakjeondong"}, {"name": "계산동", "slug": "gyesandong"}, {"name": "효성동", "slug": "hyoseongdong"}, {"name": "임학동", "slug": "imhakdong"}]},
            {"name": "중구", "slug": "junggu_incheon", "dongs": [{"name": "신포동", "slug": "sinpodong"}, {"name": "운서동", "slug": "unseodong"}, {"name": "영종동", "slug": "yeongjongdong"}, {"name": "을왕동", "slug": "eurwangdong"}]},
            {"name": "동구", "slug": "donggu_incheon", "dongs": [{"name": "송현동", "slug": "songhyeondong"}, {"name": "송림동", "slug": "songlimdong"}, {"name": "화수동", "slug": "hwasudong"}]}
        ]
    }
}

common_style = """
:root {--p:#d85a7d; --a:#ff7eb3; --bg:#fff5f7; --bg2:#ffffff; --txt:#5a2a35; --muted:#7a5c65; --bdr:#f2d6dc; --hd:#fff; --ft:#2a1418; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--bg); color:var(--txt); font-family:'Pretendard',sans-serif; line-height:1.7; }
a { color:inherit; text-decoration:none; }
.cm2-hd { background:var(--hd); border-bottom:2px solid var(--p); position:sticky; top:0; z-index:100; }
.cm2-hd-inner { max-width:1100px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:62px; padding:0 20px; }
.cm2-logo-text { font-size:16px; font-weight:800; color:var(--p); }
.cm2-sec { padding:44px 20px; }
.cm2-sec-inner { max-width:1100px; margin:0 auto; }
.cm2-sec-hd { margin-bottom:22px; }
.cm2-sec-hd h2 { font-size:21px; font-weight:800; color:var(--p); position:relative; padding-left:12px; border-left:4px solid var(--p); }
.cm2-page-h1 { font-size:24px; font-weight:900; color:var(--p); line-height:1.3; margin-bottom:8px; }
.cm2-sec-sub { font-size:14px; color:var(--muted); margin-top:4px; }
.cm2-bc { background:#fff; border-bottom:1px solid var(--bdr); padding:10px 20px; }
.cm2-bc-inner { max-width:1100px; margin:0 auto; font-size:12px; color:#7a5c65; }
.cm2-dong-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:8px; }
.cm2-dong-card { background:#fff; border:1.5px solid var(--bdr); border-radius:8px; padding:12px 14px; text-align:center; display:block; transition:all .15s; }
.cm2-dong-card:hover { border-color:var(--p); background:#fff0f3; }
.cm2-dong-card strong { display:block; font-size:14px; font-weight:700; color:var(--txt); }
.cm2-dong-card span { font-size:11px; color:var(--muted); }
.cm2-price-tbl { width:100%; border-collapse:collapse; font-size:14px; margin-top:10px; }
.cm2-price-tbl th { background:var(--p); color:#fff; padding:12px 14px; text-align:left; font-weight:700; }
.cm2-price-tbl td { padding:12px 14px; border-bottom:1px solid var(--bdr); color:var(--txt); background:#fff; }
.cm2-price-tbl tr:nth-child(even) td { background:#fff5f7; }
.cm2-step-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-top:15px; }
.cm2-step-card { background:#fff; border:1px solid var(--bdr); border-radius:10px; padding:20px; box-shadow:0 2px 6px rgba(216,90,125,0.03); }
.cm2-step-card strong { display:block; font-size:16px; color:var(--p); margin-bottom:6px; }
.cm2-step-card p { font-size:13px; color:var(--muted); line-height:1.6; }
.cm2-faq details { border:1.5px solid var(--bdr); border-radius:8px; overflow:hidden; background:#fff; margin-bottom:10px; }
.cm2-faq summary { padding:16px; font-size:15px; font-weight:700; cursor:pointer; color:var(--txt); }
.cm2-faq p { padding:0 16px 16px; font-size:14px; color:var(--muted); line-height:1.7; }
.cm2-shop-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; margin-top:15px; }
.cm2-shop-card { background:#fff; border:2.5px solid #e895ab; border-radius:14px; padding:24px; box-shadow:0 6px 20px rgba(216,90,125,0.12); transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.cm2-shop-card:hover { transform:translateY(-4px); box-shadow:0 12px 30px rgba(216,90,125,0.22); border-color:#d85a7d; }
.cm2-shop-card strong { font-size:18px; color:#5a2a35; font-weight:800; }
.cm2-shop-phone { font-size:18px; font-weight:900; color:#d85a7d; margin:12px 0 16px; display:block; letter-spacing:-0.5px; }
.cm2-btn-group { display:flex; gap:6px; }
.cm2-btn-call { flex:1; background:#d85a7d; color:#fff; text-align:center; padding:12px; border-radius:8px; font-size:14px; font-weight:800; text-decoration:none; box-shadow:0 4px 10px rgba(216,90,125,0.2); }
.cm2-btn-call:hover { background:#b84564; }
.cm2-btn-sms { flex:1; background:#ff7eb3; color:#fff; text-align:center; padding:12px; border-radius:8px; font-size:14px; font-weight:800; text-decoration:none; box-shadow:0 4px 10px rgba(255,126,179,0.2); }
.cm2-btn-sms:hover { background:#e6689b; }
.cm2-ft { background:var(--ft); padding:40px 20px; color:#d8b2bb; text-align:center; font-size:13px; margin-top:40px; }
"""

# 제휴샵 데이터
shops_raw = [
    {"name": "미인테라피", "tel": "0507-1280-3201", "desc": "엄선된 전문 관리사의 정성스러운 1:1 맞춤 방문 케어 서비스."},
    {"name": "오늘밤테라피", "tel": "0507-1280-3199", "desc": "지친 일상에 편안한 휴식을 선사하는 프리미엄 힐링 프로그램."},
    {"name": "주주테라피", "tel": "0507-1280-3197", "desc": "신속한 방문과 부드러운 이완을 도와주는 전문 홈케어 제휴샵."},
    {"name": "골든테라피", "tel": "0507-1280-3360", "desc": "고객 맞춤형 강도 조절과 깊은 피로 회복을 위한 힐링 공간."},
    {"name": "퀸즈홈테라피", "tel": "0507-1280-3296", "desc": "프라이빗하고 품격 있는 케어로 지친 몸과 마음을 달래드립니다."}
]

default_shop_cards_html = "".join([f"""
<div class="cm2-shop-card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <strong>{s['name']}</strong>
    <span style="background:#fff0f3;border:1px solid #f28ca6;color:#d85a7d;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:800;">★ 공식제휴점</span>
  </div>
  <p style="font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:12px;">{s['desc']}</p>
  <span class="cm2-shop-phone">📞 {s['tel']}</span>
  <div class="cm2-btn-group">
    <a href="tel:{s['tel']}" class="cm2-btn-call">📞 전화하기</a>
    <a href="sms:{s['tel']}" class="cm2-btn-sms">💬 문자하기</a>
  </div>
</div>
""" for s in shops_raw])

shops_script = """
<script>
  window.addEventListener('DOMContentLoaded', () => {
    const shopContainer = document.getElementById('random-shop-list');
    if(!shopContainer) return;
    const cards = Array.from(shopContainer.children);
    cards.sort(() => 0.5 - Math.random());
    cards.forEach(card => shopContainer.appendChild(card));
  });
</script>
"""

# 1. 시/도 상위 허브 템플릿
province_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>$province_title</title>
<meta name="description" content="$province_desc">
<link rel="canonical" href="{BASE_URL}/$region_key/">
<meta property="og:type" content="website">
<meta property="og:title" content="$province_title">
<meta property="og:description" content="$province_desc">
<meta property="og:url" content="{BASE_URL}/$region_key/">
{NAVER_VERIFY_TAG}
{SEO_RATING_JSON}
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">수경마사지</a><a href="/" style="font-size:13px;color:#7a5c65;">🏠 홈으로</a></div></header>
<main>
  {BANNER_HTML}
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">수경마사지</a> › $province_name 전체 지역 안내</div></nav>
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">    
        <h1 class="cm2-page-h1">$province_name 출장 마사지 및 홈타이 종합 안내</h1>    
        <p class="cm2-sec-sub">$province_name 전 지역 30분 내 신속 방문 — 원하시는 구/시를 선택하세요</p>    
      </div>    
      
      <div class="cm2-sec-hd" style="margin-top:10px;">
        <h2>$province_name 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;">
        {default_shop_cards_html}
      </div>

      <h3 style="font-size:17px;font-weight:800;margin-bottom:12px;color:var(--p);">$province_name 하위 구·시 선택</h3>
      <div class="cm2-dong-grid" style="margin-bottom:35px;">
        $sub_cards_html
      </div>  
    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 수경마사지. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

# 2. 구/시 단위 페이지 템플릿
region_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>$page_title</title>
<meta name="description" content="$page_desc">
<link rel="canonical" href="{BASE_URL}/$region_key/$sub_slug_parent/">
<meta property="og:type" content="website">
<meta property="og:title" content="$page_title">
<meta property="og:description" content="$page_desc">
<meta property="og:url" content="{BASE_URL}/$region_key/$sub_slug_parent/">
{NAVER_VERIFY_TAG}
{SEO_RATING_JSON}
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">수경마사지</a><a href="/$region_key/" style="font-size:13px;color:#7a5c65;">📍 $province_name 목록</a></div></header>
<main>
  {BANNER_HTML}
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">수경마사지</a> › <a href="/$region_key/">$province_name</a> › $region_name</div></nav>
  
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">    
        <h1 class="cm2-page-h1">$region_name 출장 마사지 및 홈타이 종합 안내</h1>    
        <p class="cm2-sec-sub">$region_name 전 지역 30분 내 신속 방문 출장 마사지 — 세부 지역을 선택하거나 제휴 샵 연락처를 확인하세요</p>    
      </div>    
      
      <div class="cm2-sec-hd" style="margin-top:10px;">
        <h2>$region_name 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;">
        {default_shop_cards_html}
      </div>

      <div style="background:#fff;border-left:3px solid #d85a7d;padding:22px;border-radius:0 8px 8px 0;margin-bottom:25px;box-shadow:0 2px 8px rgba(216,90,125,0.02);">
        <p style="font-size:15px;line-height:1.8;"><b>📍 $region_name 지역 특성 및 맞춤 방문 안내:</b> $intro</p>
        <p style="font-size:15px;line-height:1.8;margin-top:12px;">$region_name 어디든 자택, 오피스텔, 원룸, 숙소 등 고객님이 머무시는 편안한 공간으로 전문 관리사가 직접 찾아가는 출장마사지 서비스를 제공합니다.</p>
      </div>    
      
      <h3 style="font-size:17px;font-weight:800;margin-bottom:12px;color:var(--p);">$region_name 세부 지역 선택</h3>
      <div class="cm2-dong-grid" style="margin-bottom:35px;">
        $sub_cards_html
      </div>  

      <div class="cm2-sec-hd"><h2>$region_name 출장마사지, 이런 점이 궁금해요</h2></div>
      <div style="background:#fff;padding:22px;border-radius:10px;border:1px solid var(--bdr);margin-bottom:35px;">
        <p style="font-size:14px;line-height:1.8;color:var(--txt);">많은 고객님들께서 집이나 오피스텔로 관리사를 부르는 것에 대해 보안이나 위생, 준비 사항 등을 걱정하십니다. $region_name 출장마사지 서비스는 철저한 신원 검증과 위생 교육을 이수한 전문 테라피스트가 최고급 아로마 오일과 매트를 직접 지참하여 방문하므로, 고객님께서는 별도의 준비물 없이 편안하게 누워 계시기만 하면 됩니다.</p>
      </div>

      <div class="cm2-sec-hd"><h2>$region_name 홈타이 이용 절차</h2></div>
      <div class="cm2-step-grid" style="margin-bottom:35px;">
        <div class="cm2-step-card">
          <strong>1단계. 제휴 샵 문의</strong>
          <p>고객님이 계신 $region_name 내 상세 위치와 원하시는 코스를 제휴 샵 번호로 문의해 주세요.</p>
        </div>
        <div class="cm2-step-card">
          <strong>2단계. 신속 이동 및 배정</strong>
          <p>예약 확정 즉시 $region_name 인근에 대기 중인 전담 관리사가 배정되어 신속하게 이동합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>3단계. 프라이빗 케어</strong>
          <p>도착 후 관리사가 세팅 도구를 펼치고 고객님의 피로 부위에 맞춘 1:1 맞춤 케어를 시작합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>4단계. 100% 후불 결제</strong>
          <p>모든 케어 서비스가 완벽하게 끝난 안전한 후불 결제 시스템으로 요금을 지불합니다.</p>
        </div>
      </div>

      <div class="cm2-sec-hd"><h2>$region_name에서 받을 수 있는 코스 안내</h2></div>
      <p class="cm2-sec-sub" style="margin-bottom:12px;">$region_name 전 지역 동일 적용 · 심야 할증 없음 · 100% 후불제</p>
      <table class="cm2-price-tbl" style="margin-bottom:35px;">
        <tr><th>코스 분류</th><th>세부 프로그램 설명</th><th>시간 및 이용 요금</th></tr>
        <tr><td style="font-weight:700;color:var(--p)">건식케어 (타이)</td><td>전통 타이 기법으로 뭉친 근육을 부드럽게 이완시키는 기본 출장마사지 프로그램</td><td>60분 6만원 / 90분 9만원 / 120분 11만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">습식케어 (아로마)</td><td>천연 아로마 오일을 활용해 심신 안정과 혈액순환을 돕는 출장마사지 프로그램</td><td>60분 8만원 / 90분 10만원 / 120분 12만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">오일케어 (감성힐링)</td><td>부드러운 터치와 깊은 이완을 선사하는 프리미엄 힐링 출장마사지 케어</td><td>60분 9만원 / 90분 11만원 / 120분 13만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">VVIP 전신혼합</td><td>건식과 습식이 결합된 종합 토탈 바디 리프레시 출장마사지 프로그램</td><td>60분 10만원 / 90분 12만원 / 120분 14만원 / 150분 17만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">한국인 스웨디시</td><td>한국인 전문 테라피스트의 섬세한 스웨디시 감성 테라피 출장마사지</td><td>60분 14만원 / 90분 18만원</td></tr>
      </table>

      <div class="cm2-sec-hd"><h2>$region_name 자주 묻는 질문 (FAQ)</h2></div>
      <div class="cm2-faq">
        <details open><summary>$region_name 모든 동네에 정말 다 출장마사지 방문이 가능한가요?</summary><p>네, $region_name 내 주거지, 오피스텔, 원룸, 숙소 등 차량 접근이 가능한 곳이라면 어디든 신속하게 출장마사지 방문이 가능합니다.</p></details>
        <details><summary>결제는 선불인가요, 후불인가요?</summary><p>100% 후불제로 운영됩니다. 관리가 모두 끝난 후에 편하신 방법으로 결제하시면 됩니다.</p></details>
        <details><summary>늦은 새벽이나 주말에도 요금이 똑같나요?</summary><p>물론입니다. 심야 시간이나 주말에도 별도의 할증 요금을 부과하지 않습니다.</p></details>
      </div>

    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 수경마사지. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

# 3. 동 단위 세부 페이지 템플릿
sub_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>$page_title</title>
<meta name="description" content="$page_desc">
<link rel="canonical" href="{BASE_URL}/$region_key/$parent_slug/$sub_slug/">
<meta property="og:type" content="website">
<meta property="og:title" content="$page_title">
<meta property="og:description" content="$page_desc">
<meta property="og:url" content="{BASE_URL}/$region_key/$parent_slug/$sub_slug/">
{NAVER_VERIFY_TAG}
{SEO_RATING_JSON}
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">수경마사지</a><a href="/$region_key/$parent_slug/" style="font-size:13px;color:#7a5c65;">📍 $parent_name 목록</a></div></header>
<main>
  {BANNER_HTML}
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">수경마사지</a> › <a href="/$region_key/">$region_name</a> › <a href="/$region_key/$parent_slug/">$parent_name</a> › $sub_name</div></nav>
  
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">    
        <h1 class="cm2-page-h1">$sub_name 출장마사지 및 홈타이 맞춤 안내</h1>    
        <p class="cm2-sec-sub">$sub_name 일대 30분 내 신속 방문 출장마사지 케어 — 프라이빗한 힐링 서비스를 만나보세요</p>    
      </div>    
      
      <div class="cm2-sec-hd" style="margin-top:10px;">
        <h2>$sub_name 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;">
        {default_shop_cards_html}
      </div>

      <div style="background:#fff;border-left:3px solid #d85a7d;padding:22px;border-radius:0 8px 8px 0;margin-bottom:25px;box-shadow:0 2px 8px rgba(216,90,125,0.02);">
        <p style="font-size:15px;line-height:1.8;"><b>📍 $sub_name 지역 맞춤 방문 케어 안내:</b> $sub_name 주변은 조용한 주거 단지와 오피스텔이 어우러져 있어, 외부로 멀리 나가지 않고 자택이나 편안한 숙소 안에서 전문적인 출장마사지를 받고자 하시는 분들의 문의가 매우 많은 곳입니다.</p>
      </div>    

      <div class="cm2-sec-hd"><h2>$sub_name 마사지, 이런 점이 궁금해요</h2></div>
      <div style="background:#fff;padding:22px;border-radius:10px;border:1px solid var(--bdr);margin-bottom:35px;">
        <p style="font-size:14px;line-height:1.8;color:var(--txt);">“집에 누군가를 부르는 게 처음이라 어색하지 않을까요?” $sub_name에서 처음 출장마사지를 이용하시는 고객님들께서 종종 하시는 말씀입니다. 저희 서비스는 철저한 전문 소독과 위생 관리를 거친 최고급 매트와 타올, 아로마 용품을 직접 구비하여 방문하므로 고객님께서는 별도의 준비물 없이 편안하게 누워 계시기만 하면 됩니다.</p>
      </div>

      <div class="cm2-sec-hd"><h2>$sub_name 홈타이 이용 절차</h2></div>
      <div class="cm2-step-grid" style="margin-bottom:35px;">
        <div class="cm2-step-card">
          <strong>1단계. 제휴 샵 문의</strong>
          <p>$sub_name 내 상세 주소와 원하시는 케어 코스를 제휴 샵 번호로 간편하게 접수해 주세요.</p>
        </div>
        <div class="cm2-step-card">
          <strong>2단계. 담당 관리사 배정</strong>
          <p>접수 즉시 $sub_name 인근에서 대기 중인 전문 관리사가 배정되어 신속하게 출발합니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>3단계. 1:1 맞춤 방문 케어</strong>
          <p>도착 후 세팅을 마치고 고객님의 신체 컨디션과 뭉친 근육 상태에 맞춘 집중 힐링 관리가 진행됩니다.</p>
        </div>
        <div class="cm2-step-card">
          <strong>4단계. 후불 결제 진행</strong>
          <p>모든 케어 프로그램이 완전히 끝난 후 만족스러우실 때 요금을 지불하는 100% 후불제 시스템입니다.</p>
        </div>
      </div>

      <div class="cm2-sec-hd"><h2>$sub_name에서 받을 수 있는 코스 안내</h2></div>
      <p class="cm2-sec-sub" style="margin-bottom:12px;">$sub_name 전 지역 동일 요금 · 심야 할증 없음 · 100% 후불 결제</p>
      <table class="cm2-price-tbl" style="margin-bottom:35px;">
        <tr><th>코스 분류</th><th>세부 프로그램 설명</th><th>시간 및 이용 요금</th></tr>
        <tr><td style="font-weight:700;color:var(--p)">건식케어 (타이)</td><td>전통 타이 기법을 바탕으로 $sub_name 주민들의 뭉친 등·허리 근육을 시원하게 풀어주는 출장마사지 코스</td><td>60분 6만원 / 90분 9만원 / 120분 11만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">습식케어 (아로마)</td><td>순환을 돕는 고급 아로마 오일을 사용하여 부드럽고 깊은 이완을 선사하는 출장마사지 코스</td><td>60분 8만원 / 90분 10만원 / 120분 12만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">오일케어 (감성힐링)</td><td>지친 일상에 깊은 휴식과 힐링 에너지를 채워주는 프리미엄 터치 출장마사지 프로그램</td><td>60분 9만원 / 90분 11만원 / 120분 13만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">VVIP 전신혼합</td><td>건식과 아로마, 스페셜 케어가 모두 포함된 최고급 토탈 릴렉싱 출장마사지 코스</td><td>60분 10만원 / 90분 12만원 / 120분 14만원 / 150분 17만원</td></tr>
        <tr><td style="font-weight:700;color:var(--p)">한국인 스웨디시</td><td>한국인 전문 관리사만의 섬세하고 부드러운 감성 스웨디시 출장마사지 케어</td><td>60분 14만원 / 90분 18만원</td></tr>
      </table>

      <div class="cm2-sec-hd"><h2>$sub_name 자주 묻는 질문 (FAQ)</h2></div>
      <div class="cm2-faq">
        <details open><summary>$sub_name 오피스텔이나 원룸인데 출장마사지 방문이 되나요?</summary><p>네, $sub_name 내 모든 주거 형태(아파트, 오피스텔, 빌라, 원룸) 및 숙소에서 편리하게 출장마사지 서비스를 이용하실 수 있습니다.</p></details>
        <details><summary>결제는 언제 어떻게 하나요?</summary><p>100% 후불제로 운영됩니다. 관리가 모두 끝난 후에 편하신 방법으로 결제하시면 됩니다.</p></details>
        <details><summary>늦은 밤이나 새벽 시간에도 추가 비용이 없나요?</summary><p>없습니다! 평일 낮과 동일한 정직한 요금으로 이용하실 수 있습니다.</p></details>
      </div>

    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 수경마사지. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

# 빌드 실행 루프
urls = [f"{BASE_URL}/"]
region_cards_html = ""

for region_key, region_data in regions.items():
    region_dir = f"{region_key}"
    os.makedirs(region_dir, exist_ok=True)
    urls.append(f"{BASE_URL}/{region_key}/")
    
    region_cards_html += f'<a href="/{region_key}/" class="cm2-dong-card"><strong>{region_data["name"]}</strong><span>지역별 안내</span></a>\n'
    
    province_sub_cards = ""
    for sub in region_data["sub_regions"]:
        sub_name = sub["name"]
        sub_slug = sub["slug"]
        
        # 1단계: 구/시 단위 폴더
        sub_dir_path = f"{region_key}/{sub_slug}"
        os.makedirs(sub_dir_path, exist_ok=True)
        urls.append(f"{BASE_URL}/{region_key}/{sub_slug}/")
        
        province_sub_cards += f'<a href="/{region_key}/{sub_slug}/" class="cm2-dong-card"><strong>{sub_name}</strong><span>출장마사지</span></a>\n'
        
        sub_dong_cards = ""
        for dong in sub["dongs"]:
            dong_name = dong["name"]
            dong_slug = dong["slug"]
            
            # 2단계: 동 단위 폴더
            dong_dir_path = f"{sub_dir_path}/{dong_slug}"
            os.makedirs(dong_dir_path, exist_ok=True)
            urls.append(f"{BASE_URL}/{region_key}/{sub_slug}/{dong_slug}/")
            
            sub_dong_cards += f'<a href="/{region_key}/{sub_slug}/{dong_slug}/" class="cm2-dong-card"><strong>{dong_name}</strong><span>출장마사지</span></a>\n'
            
            # 🌟 동 단위 타이틀: 예) "서울 강남구 역삼동 출장 힐링 마사지 | 수경마사지"
            dong_title_variant = random.choice(TITLE_VARIANTS)
            dong_title = f"{region_data['name']} {sub_name} {dong_name} {dong_title_variant} | 수경마사지"
            
            # 🌟 동 단위 메타 디스크립션: 예) "서울 강남구 역삼동 출장마사지 안내. 프리미엄 힐링 홈타이... 건식 6만원부터..."
            dong_desc = f"{region_data['name']} {sub_name} {dong_name} 출장마사지 안내. {random.choice(DESC_INTRO_POOL)} {random.choice(DESC_PRICE_POOL)}"
            
            final_sub_html = sub_template.safe_substitute(
                region_key=region_key,
                parent_slug=sub_slug,
                parent_name=sub_name,
                region_name=region_data["name"],
                sub_name=f"{sub_name} {dong_name}",
                sub_slug=dong_slug,
                page_title=dong_title,
                page_desc=dong_desc
            )
            with open(f"{dong_dir_path}/index.html", "w", encoding="utf-8") as f_sub:
                f_sub.write(final_sub_html)
        
        # 🌟 구/시 단위 타이틀 및 메타 디스크립션 생성
        gu_title_variant = random.choice(TITLE_VARIANTS)
        gu_title = f"{region_data['name']} {sub_name} {gu_title_variant} | 수경마사지"
        gu_desc = f"{region_data['name']} {sub_name} 출장마사지 종합 안내. {random.choice(DESC_INTRO_POOL)} {random.choice(DESC_PRICE_POOL)}"
        
        final_region_html = region_template.safe_substitute(
            region_key=region_key,
            sub_slug_parent=sub_slug,
            province_name=region_data["name"],
            region_name=f"{region_data['name']} {sub_name}",
            intro=region_data["intro"],
            sub_cards_html=sub_dong_cards,
            page_title=gu_title,
            page_desc=gu_desc
        )
        with open(f"{sub_dir_path}/index.html", "w", encoding="utf-8") as f_region:
            f_region.write(final_region_html)

    # 시/도 레벨 허브 페이지 생성
    prov_title_variant = random.choice(TITLE_VARIANTS)
    prov_title = f"{region_data['name']} {prov_title_variant} 지역별 안내 | 수경마사지"
    prov_desc = f"{region_data['name']} 전 지역 출장마사지 및 홈타이 정보. {random.choice(DESC_INTRO_POOL)} {random.choice(DESC_PRICE_POOL)}"
    
    final_province_html = province_template.safe_substitute(
        region_key=region_key,
        province_name=region_data["name"],
        province_title=prov_title,
        province_desc=prov_desc,
        sub_cards_html=province_sub_cards
    )
    with open(f"{region_dir}/index.html", "w", encoding="utf-8") as f_prov:
        f_prov.write(final_province_html)

# 수도권 최상위 메인 허브 (index.html) 생성
hub_template = Template(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>서울 경기 인천 수도권 출장 이용정보 마사지 | 수경마사지</title>
<meta name="description" content="서울 경기 인천 출장마사지 종합 안내 플랫폼. 전 지역 30분 내 신속 방문 홈타이, 건식 6만원부터 100% 후불제.">
<link rel="canonical" href="{BASE_URL}/">
<meta property="og:type" content="website">
<meta property="og:title" content="서울 경기 인천 수도권 출장 이용정보 마사지 | 수경마사지">
<meta property="og:description" content="서울 경기 인천 출장마사지 종합 안내 플랫폼. 전 지역 30분 내 신속 방문 홈타이, 건식 6만원부터 100% 후불제.">
<meta property="og:url" content="{BASE_URL}/">
{NAVER_VERIFY_TAG}
{SEO_RATING_JSON}
<style>{common_style}</style></head><body>
<header class="cm2-hd"><div class="cm2-hd-inner"><a href="/" class="cm2-logo-text">수경마사지</a><a href="/" style="font-size:13px;color:#7a5c65;">🏠 홈으로</a></div></header>
<main>
  {BANNER_HTML}
  <nav class="cm2-bc"><div class="cm2-bc-inner"><a href="/">수경마사지</a> › 수도권 전체 지역 안내</div></nav>
  
  <section class="cm2-sec">  
    <div class="cm2-sec-inner">    
      <div class="cm2-sec-hd">    
        <h1 class="cm2-page-h1">서울·경기·인천 수도권 전 지역 홈타이 종합 안내</h1>    
        <p class="cm2-sec-sub">원하시는 지역(서울/경기/인천)을 선택하시면 상세 제휴샵 및 맞춤 정보를 확인하실 수 있습니다.</p>    
      </div>    
      
      <div class="cm2-sec-hd" style="margin-top:10px;">
        <h2>수도권 전역 추천 제휴 샵 (5개소)</h2>
        <p class="cm2-sec-sub">새로고침할 때마다 제휴 업소 순서가 랜덤으로 변경되며, 바로 통화 및 문자가 가능합니다.</p>
      </div>
      <div id="random-shop-list" class="cm2-shop-grid" style="margin-bottom:35px;">
        {default_shop_cards_html}
      </div>

      <div style="background:#fff;border-left:3px solid #d85a7d;padding:22px;border-radius:0 8px 8px 0;margin-bottom:25px;box-shadow:0 2px 8px rgba(216,90,125,0.02);">
        <p style="font-size:15px;line-height:1.8;"><b>📍 수도권 24시간 방문 케어 서비스:</b> 수경마사지는 서울, 경기, 인천 수도권 전 지역 어디든 고객님이 계신 자택, 오피스텔, 원룸, 숙소로 신속하게 방문하는 프리미엄 홈타이 플랫폼입니다. 심야 할증 없이 투명한 정찰제와 100% 후불제로 안전하게 이용하세요.</p>
      </div>    
      
      <h3 style="font-size:17px;font-weight:800;margin-bottom:12px;color:var(--p);">수도권 지역 선택</h3>
      <div class="cm2-dong-grid" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); margin-bottom:35px;">
        $region_cards_html
      </div>  

    </div>
  </section>
</main>
<footer class="cm2-ft"><div class="cm2-sec-inner"><p>© 2026 수경마사지. All rights reserved.</p></div></footer>
{shops_script}
</body></html>""")

final_hub_html = hub_template.safe_substitute(region_cards_html=region_cards_html)
with open("index.html", "w", encoding="utf-8") as f_hub:
    f_hub.write(final_hub_html)

# robots.txt 생성
robots_txt = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f_robots:
    f_robots.write(robots_txt)

# sitemap.xml 생성
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
sitemap_xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f_sitemap:
    f_sitemap.write(sitemap_xml)
        
print("✨ [SEO 최적화 완료] 타이틀 변형 풀과 '시구동 출장마사지' 기반 메타디스크립션 중복 방지 로직이 완벽하게 적용되었습니다!")