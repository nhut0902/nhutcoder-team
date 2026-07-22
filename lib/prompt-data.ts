// Prompt store data

export interface Prompt {
  slug: string;
  title: string;
  description: string;
  category: string;
  content: string;
  tags: string[];
  price: number;
  uses: number;
  rating: number;
}

export const PROMPTS: Prompt[] = [
  {
    slug: "code-review-ai",
    title: "AI Code Review",
    description: "Prompt AI review code chuyên sâu — tìm bug, đề xuất tối ưu, giải thích code.",
    category: "Code",
    content: "Bạn là một senior code reviewer. Hãy review đoạn code sau:\n\n1. Tìm bugs và lỗ hổng bảo mật\n2. Đề xuất tối ưu hiệu năng\n3. Giải thích code ngắn gọn\n4. Đưa ra phiên bản cải thiện\n\nCode: [PASTE CODE HERE]",
    tags: ["Code Review", "Bug", "Tối ưu"],
    price: 0,
    uses: 1234,
    rating: 4.9,
  },
  {
    slug: "vietnamese-content",
    title: "Viết Content Tiếng Việt",
    description: "Tạo content marketing tiếng Việt tự nhiên, thu hút, chuẩn SEO.",
    category: "Content",
    content: "Bạn là copywriter tiếng Việt chuyên nghiệp. Viết content [LOẠI CONTENT] về [CHỦ ĐỀ] với:\n\n- Tiêu đề thu hút\n- Mở bài gợi tò mò\n- Thân bài có cấu trúc rõ ràng\n- Kết bài có CTA\n- Tối ưu SEO từ khóa: [TỪ KHÓA]\n- Độ dài: [SỐ TỪ] từ",
    tags: ["Marketing", "SEO", "Tiếng Việt"],
    price: 0,
    uses: 892,
    rating: 4.8,
  },
  {
    slug: "game-design-doc",
    title: "Game Design Document",
    description: "Tạo GDD hoàn chỉnh cho game — gameplay, story, characters, mechanics.",
    category: "Game",
    content: "Bạn là game designer chuyên nghiệp. Tạo Game Design Document cho game [TÊN GAME]:\n\n1. Tổng quan game\n2. Cốt truyện\n3. Nhân vật chính\n4. Gameplay mechanics\n5. Level design\n6. UI/UX\n7. Monetization\n8. Technical specs",
    tags: ["Game Design", "GDD", "Game Dev"],
    price: 29,
    uses: 456,
    rating: 4.7,
  },
  {
    slug: "api-design",
    title: "REST API Design",
    description: "Thiết kế REST API chuẩn — endpoints, schemas, authentication, documentation.",
    category: "Code",
    content: "Bạn là API architect. Thiết kế REST API cho [DỰ ÁN]:\n\n1. Danh sách endpoints (CRUD)\n2. Request/Response schemas\n3. Authentication method\n4. Error handling\n5. Rate limiting\n6. OpenAPI spec\n7. Example requests",
    tags: ["API", "REST", "Backend"],
    price: 19,
    uses: 678,
    rating: 4.9,
  },
  {
    slug: "youtube-script",
    title: "Kịch Bản YouTube",
    description: "Viết kịch bản YouTube video tiếng Việt — intro thu hút, nội dung, outro.",
    category: "Content",
    content: "Bạn là YouTube scriptwriter. Viết kịch bản video [CHỦ ĐỀ]:\n\n- Hook (15 giây đầu)\n- Intro\n- Nội dung chính (có timestamp)\n- B-roll suggestions\n- Outro + CTA\n- Tiêu đề + mô tả + tags SEO\n\nĐộ dài: [SỐ PHÚT] phút",
    tags: ["YouTube", "Video", "Tiếng Việt"],
    price: 0,
    uses: 1023,
    rating: 4.8,
  },
  {
    slug: "ui-ux-review",
    title: "UI/UX Review",
    description: "Review giao diện — tìm vấn đề UX, đề xuất cải thiện, accessibility.",
    category: "Design",
    content: "Bạn là UI/UX expert. Review giao diện [URL/MÔ TẢ]:\n\n1. Vấn đề usability\n2. Accessibility (WCAG)\n3. Visual hierarchy\n4. Mobile responsiveness\n5. Performance\n6. Đề xuất cải thiện (ưu tiên theo impact)",
    tags: ["UI", "UX", "Design"],
    price: 15,
    uses: 345,
    rating: 4.6,
  },
  {
    slug: "sql-optimizer",
    title: "SQL Query Optimizer",
    description: "Tối ưu SQL query — phân tích, đề xuất index, rewrite cho hiệu năng.",
    category: "Code",
    content: "Bạn là database expert. Tối ưu SQL query sau:\n\n[SQL QUERY]\n\n1. Phân tích execution plan\n2. Tìm bottleneck\n3. Đề xuất index\n4. Rewrite query tối ưu\n5. Giải thích thay đổi",
    tags: ["SQL", "Database", "Tối ưu"],
    price: 10,
    uses: 567,
    rating: 4.7,
  },
  {
    slug: "startup-pitch",
    title: "Startup Pitch Deck",
    description: "Tạo pitch deck startup — problem, solution, market, business model.",
    category: "Business",
    content: "Bạn là pitch deck consultant. Tạo pitch deck cho startup [TÊN]:\n\n1. Problem\n2. Solution\n3. Market size\n4. Business model\n5. Traction\n6. Team\n7. Financials\n8. Ask (funding)\n\nMỗi slide: tiêu đề + nội dung + visual suggestion",
    tags: ["Startup", "Pitch", "Business"],
    price: 25,
    uses: 234,
    rating: 4.8,
  },
];

export const PROMPT_CATEGORIES = ["Tất cả", "Code", "Content", "Game", "Design", "Business"];
