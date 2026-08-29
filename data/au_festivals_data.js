// 澳洲节日选品数据库 —— product-radar-au 专用
// 结构与UK版 festivals_data.js 完全一致（festival_engine 直接解析）
// 红线约束：无液体/膏体、无body care、无电器灯具、轻小件≤200g/包装≤30×21×6cm
// 价格带：A$8.99-16.99（成本¥4-8，汇率 1 AUD ≈ 4.8 CNY，2026-08-29 与 config.json 对齐）
// 利润标注口径：按价格带上限（~A$16.99）的三项硬成本（佣金+FBA+采购）估算；
//   下限价格利润率会收窄到 20% 附近，新增 SKU 定价优先取带上限区间
// 反季要点：圣诞=盛夏（海滩主题）、Back to School在1月底、母亲节5月/父亲节9月

const FESTIVALS = [
  {
    "id": "fathers-day-au-2026",
    "name": "父亲节(澳洲)",
    "nameEn": "",
    "icon": "👔",
    "date": "2026-09-06",
    "month": 9,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "DIY工具收纳腰带",
        "category": "gift",
        "margin": "约50-62%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "tool belt",
          "tool organiser",
          "gifts for dad diy"
        ],
        "sourcing": "1688: 工具收纳腰包"
      },
      {
        "sku": "车载应急包(小件)",
        "category": "gift",
        "margin": "约48-58%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "car emergency kit",
          "roadside kit"
        ],
        "sourcing": "1688: 车载应急包"
      },
      {
        "sku": "BBQ工具套装(5件内)",
        "category": "gift",
        "margin": "约50-60%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 多件套装 5pcs (≥5件, 包装易超标)",
        "keywords": [
          "bbq tools set",
          "grill accessories set"
        ],
        "sourcing": "1688: BBQ工具套装"
      },
      {
        "sku": "磁力腕带螺丝刀托",
        "category": "gift",
        "margin": "约55-65%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "magnetic wristband",
          "screw holder wrist"
        ],
        "sourcing": "1688: 磁力腕带工具"
      },
      {
        "sku": "皮革钥匙扣DIY套件",
        "category": "gift",
        "margin": "约52-63%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "leather keychain kit",
          "dad craft gift"
        ],
        "sourcing": "1688: 皮革钥匙扣材料包"
      }
    ]
  },
  {
    "id": "spring-start-footy-2026",
    "name": "初春+橄榄球决赛月",
    "nameEn": "",
    "icon": "🏉",
    "date": "2026-09-01",
    "month": 9,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "观赛零食分格盘",
        "category": "home",
        "margin": "约52-62%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 snack",
        "keywords": [
          "snack tray",
          "party serving tray"
        ],
        "sourcing": "1688: 分格零食盘"
      },
      {
        "sku": "野餐垫防水折叠",
        "category": "outdoor",
        "margin": "约48-58%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "picnic blanket",
          "waterproof picnic mat foldable"
        ],
        "sourcing": "1688: 防水野餐垫"
      },
      {
        "sku": "充气饮料保冷桶",
        "category": "outdoor",
        "margin": "约50-60%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 drink",
        "keywords": [
          "inflatable cooler",
          "drink bucket party"
        ],
        "sourcing": "1688: 充气保冷桶"
      }
    ]
  },
  {
    "id": "school-holidays-spring-2026",
    "name": "春假(9月中-10月初)",
    "nameEn": "",
    "icon": "🎒",
    "date": "2026-09-19",
    "month": 9,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "儿童户外探索玩具包",
        "category": "kids",
        "margin": "约50-60%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 toy (非宠物/节日)",
        "keywords": [
          "kids explorer kit",
          "outdoor adventure toys"
        ],
        "sourcing": "1688: 儿童探索玩具套装"
      },
      {
        "sku": "旅行游戏便携装",
        "category": "kids",
        "margin": "约53-63%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "travel games for kids",
          "road trip activities"
        ],
        "sourcing": "1688: 便携旅行桌游"
      },
      {
        "sku": "手工黏土工具模具组",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "clay tools kids",
          "playdough accessories"
        ],
        "sourcing": "1688: 黏土工具模具"
      }
    ]
  },
  {
    "id": "labour-day-nsw-2026",
    "name": "劳动节长周末(NSW)",
    "nameEn": "",
    "icon": "🏕️",
    "date": "2026-10-05",
    "month": 10,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "露营餐具折叠套装",
        "category": "outdoor",
        "margin": "约54-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "camping cutlery set",
          "foldable utensils travel"
        ],
        "sourcing": "1688: 折叠露营餐具"
      },
      {
        "sku": "户外防水收纳袋",
        "category": "outdoor",
        "margin": "约56-65%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "dry bag",
          "waterproof pouch camping"
        ],
        "sourcing": "1688: 防水收纳袋"
      },
      {
        "sku": "便携吊床轻量款",
        "category": "outdoor",
        "margin": "约48-58%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "portable hammock",
          "lightweight hammock"
        ],
        "sourcing": "1688: 降落伞布吊床"
      }
    ]
  },
  {
    "id": "grand-final-day-2026",
    "name": "AFL总决赛日",
    "nameEn": "",
    "icon": "🏟️",
    "date": "2026-09-26",
    "month": 9,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "一次性观赛派对餐具组",
        "category": "gift",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "game day party supplies",
          "footy party plates"
        ],
        "sourcing": "1688: 运动派对纸餐具"
      },
      {
        "sku": "充气橄榄球玩具",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 3,
        "riskNote": "⚠️待复核 toy (非宠物/节日)",
        "keywords": [
          "inflatable football toy",
          "footy ball kids"
        ],
        "sourcing": "1688: 充气球类玩具"
      }
    ]
  },
  {
    "id": "halloween-au-2026",
    "name": "万圣节(增长中)",
    "nameEn": "",
    "icon": "🎃",
    "date": "2026-10-31",
    "month": 10,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "不给糖就捣蛋袋",
        "category": "gift",
        "margin": "约56-66%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "trick or treat bag",
          "halloween tote"
        ],
        "sourcing": "1688: 万圣节讨糖袋"
      },
      {
        "sku": "纸质派对装饰套装",
        "category": "decor",
        "margin": "约53-63%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "halloween decorations indoor",
          "halloween party decor kit"
        ],
        "sourcing": "1688: 万圣节纸装饰"
      },
      {
        "sku": "南瓜雕刻工具组",
        "category": "gift",
        "margin": "约55-65%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "pumpkin carving kit",
          "jack o lantern tools"
        ],
        "sourcing": "1688: 南瓜雕刻工具"
      },
      {
        "sku": "蜘蛛网弹力装饰+蜘蛛",
        "category": "decor",
        "margin": "约58-67%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "spider web halloween",
          "stretch cobweb decoration"
        ],
        "sourcing": "1688: 万圣节蜘蛛网装饰"
      },
      {
        "sku": "儿童派对拍照道具",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "photo booth props halloween",
          "party photo props"
        ],
        "sourcing": "1688: 派对拍照道具"
      }
    ]
  },
  {
    "id": "spring-racing-2026",
    "name": "春季赛马嘉年华预热",
    "nameEn": "",
    "icon": "🏇",
    "date": "2026-10-24",
    "month": 10,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "花园派对装饰串旗",
        "category": "decor",
        "margin": "约55-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "garden bunting",
          "party banner outdoor"
        ],
        "sourcing": "1688: 派对串旗"
      },
      {
        "sku": "遮阳草帽(平折款)",
        "category": "apparel",
        "margin": "约52-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "packable sun hat",
          "straw hat women foldable"
        ],
        "sourcing": "1688: 可折叠草帽"
      },
      {
        "sku": "香槟杯塑料复刻款",
        "category": "home",
        "margin": "约53-62%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "plastic champagne flutes",
          "reusable party glasses"
        ],
        "sourcing": "1688: 塑料香槟杯"
      }
    ]
  },
  {
    "id": "summer-prep-2026",
    "name": "初夏准备(10月末)",
    "nameEn": "",
    "icon": "☀️",
    "date": "2026-10-28",
    "month": 10,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "沙滩玩具收纳网袋",
        "category": "outdoor",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 toy (非宠物/节日)",
        "keywords": [
          "beach toy bag",
          "mesh beach bag kids"
        ],
        "sourcing": "1688: 沙滩玩具网袋"
      },
      {
        "sku": "车用遮阳挡前挡",
        "category": "auto",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "car sun shade windshield",
          "windshield cover"
        ],
        "sourcing": "1688: 汽车遮阳挡"
      },
      {
        "sku": "户外挂钩免打孔",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "outdoor hooks adhesive",
          "no drill hooks"
        ],
        "sourcing": "1688: 免打孔挂钩"
      }
    ]
  },
  {
    "id": "melbourne-cup-2026",
    "name": "墨尔本杯赛马日",
    "nameEn": "",
    "icon": "🥂",
    "date": "2026-11-03",
    "month": 11,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "赛马日派对装饰套装",
        "category": "decor",
        "margin": "约53-63%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "race day party supplies",
          "melbourne cup party decor"
        ],
        "sourcing": "1688: 赛马主题派对装饰"
      },
      {
        "sku": "纸扇装饰/手fan道具",
        "category": "gift",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "paper fans party",
          "race day fascinator props"
        ],
        "sourcing": "1688: 纸扇派对道具"
      },
      {
        "sku": "一次性鸡尾酒签/果签",
        "category": "home",
        "margin": "约60-68%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "cocktail picks",
          "party food picks fancy"
        ],
        "sourcing": "1688: 鸡尾酒水果签"
      }
    ]
  },
  {
    "id": "xmas-shopping-peak-2026",
    "name": "圣诞购物峰值启动(夏日圣诞)",
    "nameEn": "",
    "icon": "🎄",
    "date": "2026-11-15",
    "month": 11,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "海滩圣诞装饰系列",
        "category": "decor",
        "margin": "约52-62%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "beach christmas ornaments",
          "australian christmas decor",
          "coastal christmas"
        ],
        "sourcing": "1688: 海洋风圣诞挂饰"
      },
      {
        "sku": "圣诞袜(轻量款)",
        "category": "decor",
        "margin": "约55-65%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "christmas stockings",
          "xmas stockings large"
        ],
        "sourcing": "1688: 圣诞袜"
      },
      {
        "sku": "礼物包装纸胶带套装",
        "category": "gift",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "gift wrapping tape set",
          "christmas wrap accessories"
        ],
        "sourcing": "1688: 礼物包装胶带贴纸"
      },
      {
        "sku": "圣诞倒计时木历",
        "category": "decor",
        "margin": "约50-60%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "wooden advent calendar",
          "diy advent calendar empty"
        ],
        "sourcing": "1688: 木质圣诞倒计时盒"
      },
      {
        "sku": "圣诞餐桌垫套装",
        "category": "home",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "christmas placemats",
          "xmas table mats set"
        ],
        "sourcing": "1688: 圣诞餐垫"
      },
      {
        "sku": "圣诞袜小礼物混装",
        "category": "gift",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "stocking fillers",
          "small christmas gifts adults"
        ],
        "sourcing": "1688: 圣诞小礼品混装"
      }
    ]
  },
  {
    "id": "black-friday-2026",
    "name": "黑五网一",
    "nameEn": "",
    "icon": "🖤",
    "date": "2026-11-27",
    "month": 11,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "大促囤货组织袋",
        "category": "home",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 vacuum",
        "keywords": [
          "storage bags clothes",
          "vacuum storage bags small"
        ],
        "sourcing": "1688: 收纳袋"
      },
      {
        "sku": "桌面理线器硅胶",
        "category": "office",
        "margin": "约58-67%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "cable clips desk",
          "cord organizer silicone"
        ],
        "sourcing": "1688: 硅胶理线器"
      },
      {
        "sku": "厨房抽屉分隔收纳",
        "category": "home",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "drawer dividers adjustable",
          "kitchen drawer organiser"
        ],
        "sourcing": "1688: 可调节抽屉分隔板"
      }
    ]
  },
  {
    "id": "boxing-day-2026",
    "name": "节礼日大促",
    "nameEn": "",
    "icon": "🛍️",
    "date": "2026-12-26",
    "month": 12,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "节日后收纳整理箱",
        "category": "home",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "foldable storage boxes",
          "collapsible storage bins"
        ],
        "sourcing": "1688: 可折叠收纳箱"
      },
      {
        "sku": "夏季出行行李收纳7件套",
        "category": "travel",
        "margin": "约51-60%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 多件套装 7pcs (≥5件, 包装易超标)",
        "keywords": [
          "packing cubes travel",
          "luggage organiser set"
        ],
        "sourcing": "1688: 行李收纳七件套"
      }
    ]
  },
  {
    "id": "christmas-au-2026",
    "name": "圣诞节(盛夏版)",
    "nameEn": "",
    "icon": "🏖️",
    "date": "2026-12-25",
    "month": 12,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "沙滩毯沙袋固定款",
        "category": "outdoor",
        "margin": "约52-62%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 oversize: 关键词标记为超大体积",
        "keywords": [
          "beach blanket sandproof",
          "oversized beach mat"
        ],
        "sourcing": "1688: 防沙沙滩垫"
      },
      {
        "sku": "户外BBQ配件礼包",
        "category": "gift",
        "margin": "约50-59%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "bbq accessories gift set",
          "grill tools christmas"
        ],
        "sourcing": "1688: 烧烤配件礼盒"
      },
      {
        "sku": "充气泳池家庭款配件包",
        "category": "outdoor",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 toy (非宠物/节日)",
        "keywords": [
          "pool floats kids",
          "pool toys bundle"
        ],
        "sourcing": "1688: 泳池玩具套装"
      },
      {
        "sku": "野餐篮现代款",
        "category": "outdoor",
        "margin": "约48-56%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "picnic basket set",
          "picnic set 2 person"
        ],
        "sourcing": "1688: 野餐篮套餐"
      },
      {
        "sku": "冰镇饮料保温袋",
        "category": "outdoor",
        "margin": "约51-60%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "insulated cooler bag",
          "cooler tote leakproof"
        ],
        "sourcing": "1688: 保冷袋便当"
      },
      {
        "sku": "夏日圣诞桌旗装饰",
        "category": "decor",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "australian christmas table decor",
          "eucalyptus christmas"
        ],
        "sourcing": "1688: 桌旗圣诞装饰"
      }
    ]
  },
  {
    "id": "new-year-travel-2026",
    "name": "新年跨年旅行季",
    "nameEn": "",
    "icon": "🎉",
    "date": "2026-12-28",
    "month": 12,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "便携洗漱包悬挂式",
        "category": "travel",
        "margin": "约52-61%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "hanging toiletry bag",
          "travel organiser bathroom"
        ],
        "sourcing": "1688: 悬挂洗漱包"
      },
      {
        "sku": "护照包机票夹",
        "category": "travel",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "passport holder family",
          "travel document organiser"
        ],
        "sourcing": "1688: 护照包证件夹"
      },
      {
        "sku": "折叠旅行衣架6只装",
        "category": "travel",
        "margin": "约56-65%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "travel hangers folding",
          "portable clothes rack travel"
        ],
        "sourcing": "1688: 折叠衣架旅行"
      }
    ]
  },
  {
    "id": "school-holidays-summer-2026",
    "name": "暑期亲子季(12月中-1月底)",
    "nameEn": "",
    "icon": "🌞",
    "date": "2026-12-14",
    "month": 12,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "泡泡机手动款+补充液除外",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "giant bubble wands",
          "bubble wand set kids"
        ],
        "sourcing": "1688: 大号泡泡棒"
      },
      {
        "sku": "水上漂浮玩具",
        "category": "kids",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 toy (非宠物/节日)",
        "keywords": [
          "pool diving toys",
          "water games kids"
        ],
        "sourcing": "1688: 水上玩具"
      },
      {
        "sku": "儿童园艺工具组",
        "category": "kids",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "kids gardening tools",
          "children garden set"
        ],
        "sourcing": "1688: 儿童园艺工具"
      }
    ]
  },
  {
    "id": "back-to-school-jan-2027",
    "name": "返校季Term1(⭐最大文具节点)",
    "nameEn": "",
    "icon": "📚",
    "date": "2027-01-27",
    "month": 1,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "保温饭盒袋午餐包",
        "category": "kids",
        "margin": "约53-62%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "kids lunch bag insulated",
          "school lunch box bag"
        ],
        "sourcing": "1688: 儿童保温午餐包"
      },
      {
        "sku": "姓名贴纸防水套装",
        "category": "stationery",
        "margin": "约58-67%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "name labels school waterproof",
          "kids name stickers"
        ],
        "sourcing": "1688: 防水姓名贴"
      },
      {
        "sku": "文具铅笔盒多功能",
        "category": "stationery",
        "margin": "约55-64%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 oversize: 关键词标记为超大体积",
        "keywords": [
          "pencil case boys",
          "pencil case girls large capacity"
        ],
        "sourcing": "1688: 大容量笔袋"
      },
      {
        "sku": "儿童水壶背带",
        "category": "kids",
        "margin": "约59-68%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "drink bottle carrier strap",
          "water bottle sling kids"
        ],
        "sourcing": "1688: 水壶背带"
      },
      {
        "sku": "书包防雨罩",
        "category": "kids",
        "margin": "约58-67%",
        "matchScore": 3,
        "riskNote": "⚠️待复核",
        "keywords": [
          "backpack rain cover",
          "school bag cover waterproof"
        ],
        "sourcing": "1688: 书包防雨罩"
      },
      {
        "sku": "课桌整理支架",
        "category": "stationery",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "desk organiser kids",
          "homework station setup"
        ],
        "sourcing": "1688: 学生桌面收纳架"
      }
    ]
  },
  {
    "id": "australia-day-2027",
    "name": "澳大利亚国庆日",
    "nameEn": "",
    "icon": "🇦🇺",
    "date": "2027-01-26",
    "month": 1,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "国庆BBQ派对照料套装",
        "category": "gift",
        "margin": "约54-63%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "australia day party supplies",
          "aussie flag party decor"
        ],
        "sourcing": "1688: 国庆派对用品"
      },
      {
        "sku": "国旗元素沙滩 towel",
        "category": "outdoor",
        "margin": "约51-60%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "australian flag beach towel",
          "aussie towel"
        ],
        "sourcing": "1688: 国旗沙滩巾"
      },
      {
        "sku": "户外游戏木块叠叠乐",
        "category": "outdoor",
        "margin": "约48-57%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "outdoor block game",
          "timber tower game"
        ],
        "sourcing": "1688: 户外叠叠木"
      }
    ]
  },
  {
    "id": "summer-beach-2027",
    "name": "盛夏海滩季峰值",
    "nameEn": "",
    "icon": "🌊",
    "date": "2027-01-10",
    "month": 1,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "防水手机袋(通用)",
        "category": "travel",
        "margin": "约60-68%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "waterproof phone pouch beach",
          "dry phone case swim"
        ],
        "sourcing": "1688: 手机防水袋"
      },
      {
        "sku": "沙滩帐篷地钉配件",
        "category": "outdoor",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "beach tent stakes",
          "sand anchors canopy"
        ],
        "sourcing": "1688: 沙滩地钉"
      },
      {
        "sku": "硅藻泥速干垫(小尺寸)",
        "category": "home",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "quick dry mat",
          "diatomaceous earth bath mat small"
        ],
        "sourcing": "1688: 硅藻泥脚垫"
      },
      {
        "sku": "防晒帽绳防风扣",
        "category": "accessories",
        "margin": "约62-70%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "hat strap clip",
          "chin cord hat"
        ],
        "sourcing": "1688: 帽子防风绳"
      }
    ]
  },
  {
    "id": "lunar-new-year-2027",
    "name": "农历新年(澳洲大城市大节点)",
    "nameEn": "",
    "icon": "🏮",
    "date": "2027-02-06",
    "month": 2,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "春节红灯笼挂饰(小)",
        "category": "decor",
        "margin": "约55-64%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "chinese new year lanterns",
          "lunar new year decor"
        ],
        "sourcing": "1688: 新年灯笼挂饰"
      },
      {
        "sku": "红包袋创意款",
        "category": "gift",
        "margin": "约60-69%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "chinese red envelopes",
          "lucky money packets cute"
        ],
        "sourcing": "1688: 创意红包"
      },
      {
        "sku": "生肖主题餐垫桌饰",
        "category": "decor",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "year of the goat 2027",
          "chinese zodiac table runner"
        ],
        "sourcing": "1688: 生肖桌旗"
      },
      {
        "sku": "新年福字门贴静电贴",
        "category": "decor",
        "margin": "约60-69%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "chinese new year window clings",
          "cny decorations static"
        ],
        "sourcing": "1688: 春节静电窗贴"
      }
    ]
  },
  {
    "id": "valentines-day-2027",
    "name": "情人节",
    "nameEn": "",
    "icon": "💝",
    "date": "2027-02-14",
    "month": 2,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "情侣相框木质",
        "category": "gift",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "couple picture frame",
          "photo frame valentines gift"
        ],
        "sourcing": "1688: 木质相框"
      },
      {
        "sku": "心形烘焙模具套装",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "heart baking moulds",
          "valentine cake pan silicone"
        ],
        "sourcing": "1688: 心形烘焙模具"
      },
      {
        "sku": "浪漫烛台(无蜡烛)",
        "category": "decor",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "candle holders set",
          "table centrepiece romantic"
        ],
        "sourcing": "1688: 烛台摆件"
      },
      {
        "sku": "惊喜礼盒爆炸盒DIY",
        "category": "gift",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "explosion box kit",
          "surprise gift box diy"
        ],
        "sourcing": "1688: DIY爆炸礼盒"
      }
    ]
  },
  {
    "id": "late-summer-outdoor-2027",
    "name": "夏末户外延续",
    "nameEn": "",
    "icon": "🌴",
    "date": "2027-02-20",
    "month": 2,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "户外折叠凳便携",
        "category": "outdoor",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "folding stool lightweight",
          "portable camping stool"
        ],
        "sourcing": "1688: 超轻折叠凳"
      },
      {
        "sku": "驱蚊手环(物理)",
        "category": "outdoor",
        "margin": "约60-68%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "mosquito bracelet kids",
          "anti mosquito wristband deet free"
        ],
        "sourcing": "1688: 驱蚊手环"
      },
      {
        "sku": "野餐防虫帐食物罩",
        "category": "outdoor",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "food covers mesh outdoor",
          "picnic food tent"
        ],
        "sourcing": "1688: 户外食物罩"
      }
    ]
  },
  {
    "id": "autumn-reset-2027",
    "name": "入秋整理季",
    "nameEn": "",
    "icon": "🍂",
    "date": "2027-03-01",
    "month": 3,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "衣柜分层隔板",
        "category": "home",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 wardrobe",
        "keywords": [
          "wardrobe dividers shelf",
          "closet organisers hanging"
        ],
        "sourcing": "1688: 衣柜分隔板"
      },
      {
        "sku": "真空压缩袋手泵款",
        "category": "home",
        "margin": "约52-61%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 vacuum",
        "keywords": [
          "vacuum storage bags",
          "space saver bags pump"
        ],
        "sourcing": "1688: 真空压缩袋"
      },
      {
        "sku": "清洁刮水器手持",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "window squeegee shower",
          "glass wiper handheld"
        ],
        "sourcing": "1688: 玻璃刮水器"
      }
    ]
  },
  {
    "id": "moomba-labour-vic-2027",
    "name": "蒙巴节/维州劳动节",
    "nameEn": "",
    "icon": "🎪",
    "date": "2027-03-08",
    "month": 3,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "嘉年华派对道具",
        "category": "gift",
        "margin": "约55-64%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "carnival party favours",
          "festival props kids"
        ],
        "sourcing": "1688: 嘉年华道具"
      },
      {
        "sku": "折叠推拉购物车配件",
        "category": "outdoor",
        "margin": "约52-61%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "beach cart accessories",
          "wagon organiser bag"
        ],
        "sourcing": "1688: 推车轮具配件"
      }
    ]
  },
  {
    "id": "easter-2027",
    "name": "复活节(秋假重叠)",
    "nameEn": "",
    "icon": "🐰",
    "date": "2027-03-28",
    "month": 3,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "寻蛋编织篮",
        "category": "gift",
        "margin": "约54-63%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "easter baskets for kids",
          "egg hunt basket"
        ],
        "sourcing": "1688: 复活节篮子"
      },
      {
        "sku": "复活节装饰蛋(塑料DIY)",
        "category": "kids",
        "margin": "约56-65%",
        "matchScore": 5,
        "riskNote": "⚠️待复核",
        "keywords": [
          "plastic easter eggs fillable",
          "easter egg hunt supplies"
        ],
        "sourcing": "1688: 可开合塑料彩蛋"
      },
      {
        "sku": "兔子耳朵头饰(派对款)",
        "category": "kids",
        "margin": "约59-68%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "bunny ears headband",
          "easter dress up kids"
        ],
        "sourcing": "1688: 兔耳朵发箍"
      },
      {
        "sku": "复活节桌布(防水)",
        "category": "home",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "easter tablecloth rectangle",
          "disposable easter table cover"
        ],
        "sourcing": "1688: 复活节桌布"
      },
      {
        "sku": "春季手工彩纸套装",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "easter craft kit kids",
          "paper crafts spring"
        ],
        "sourcing": "1688: 儿童手工纸"
      }
    ]
  },
  {
    "id": "anzac-day-2027",
    "name": "澳新军团日",
    "nameEn": "",
    "icon": "🌾",
    "date": "2027-04-25",
    "month": 4,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "Anzac烘焙曲奇模具",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "anzac biscuit cutter",
          "baking set gifts"
        ],
        "sourcing": "1688: 曲奇饼干模具"
      },
      {
        "sku": "迷迭香种植盆栽套件",
        "category": "garden",
        "margin": "约53-62%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "herb growing kit",
          "rosemary planter pot"
        ],
        "sourcing": "1688: 香草种植套装"
      }
    ]
  },
  {
    "id": "school-camp-autumn-2027",
    "name": "秋季学期露营季",
    "nameEn": "",
    "icon": "⛺",
    "date": "2027-04-20",
    "month": 4,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "营地灯挂绳配件",
        "category": "outdoor",
        "margin": "约58-67%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "tent hanging straps",
          "camping hooks accessories"
        ],
        "sourcing": "1688: 帐篷挂绳挂钩"
      },
      {
        "sku": "睡袋内胆抓绒",
        "category": "outdoor",
        "margin": "约51-60%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "sleeping bag liner",
          "camp sheet fleece"
        ],
        "sourcing": "1688: 睡袋内胆"
      },
      {
        "sku": "防水地图证件袋",
        "category": "outdoor",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "waterproof map pouch",
          "document dry bag hiking"
        ],
        "sourcing": "1688: 防水文件袋"
      }
    ]
  },
  {
    "id": "mothers-day-au-2027",
    "name": "母亲节(澳洲5月)",
    "nameEn": "",
    "icon": "💐",
    "date": "2027-05-09",
    "month": 5,
    "importance": "S",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "珠宝收纳盒旅行款",
        "category": "gift",
        "margin": "约52-61%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "jewellery box travel",
          "jewelry organiser mum gift"
        ],
        "sourcing": "1688: 旅行首饰盒"
      },
      {
        "sku": "花园妈妈工具围裙",
        "category": "garden",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "garden apron women pockets",
          "mum gardening gift"
        ],
        "sourcing": "1688: 园艺围裙"
      },
      {
        "sku": "早餐托盘竹木折叠腿",
        "category": "home",
        "margin": "约48-56%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "bed tray breakfast folding",
          "bamboo serving tray lap"
        ],
        "sourcing": "1688: 折叠腿床上小桌板"
      },
      {
        "sku": "手部按摩滚轮(非电动)",
        "category": "wellness",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "hand roller massager manual",
          "muscle roller sticks"
        ],
        "sourcing": "1688: 手动按摩滚轮"
      },
      {
        "sku": "香薰石扩香摆件(无液体)",
        "category": "decor",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "aroma stone plaster",
          "passive diffuser ornament"
        ],
        "sourcing": "1688: 石膏扩香石"
      },
      {
        "sku": "保温杯茶漏一体",
        "category": "home",
        "margin": "约50-59%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 mug",
        "keywords": [
          "tea infuser bottle glass",
          "brewing bottle travel mug"
        ],
        "sourcing": "1688: 泡茶杯过滤"
      }
    ]
  },
  {
    "id": "autumn-fishing-2027",
    "name": "秋钓季开启",
    "nameEn": "",
    "icon": "🎣",
    "date": "2027-05-15",
    "month": 5,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "路亚饵盒透明收纳",
        "category": "outdoor",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "tackle box organiser",
          "lure storage case"
        ],
        "sourcing": "1688: 路亚盒"
      },
      {
        "sku": "保温壶大容量户外",
        "category": "outdoor",
        "margin": "约49-57%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "thermos flask 1l",
          "insulated flask hiking"
        ],
        "sourcing": "1688: 大容量保温壶"
      },
      {
        "sku": "钓鱼手套防刺",
        "category": "outdoor",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "fishing gloves men",
          "cut resistant gloves fishing"
        ],
        "sourcing": "1688: 钓鱼手套"
      }
    ]
  },
  {
    "id": "eofy-2027",
    "name": "财年末EOFY(⭐澳独有)",
    "nameEn": "",
    "icon": "💼",
    "date": "2027-06-30",
    "month": 6,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "办公桌面文件架",
        "category": "office",
        "margin": "约53-62%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "desk file organiser",
          "office paper tray stackable"
        ],
        "sourcing": "1688: 文件收纳架"
      },
      {
        "sku": "发票收据分类夹",
        "category": "office",
        "margin": "约55-64%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "receipt organiser file",
          "expanding file folder tax"
        ],
        "sourcing": "1688: 发票收纳册"
      },
      {
        "sku": "计算器文具礼盒(办公)",
        "category": "office",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "desk accessories set office",
          "stationery organiser set"
        ],
        "sourcing": "1688: 办公文具套装"
      }
    ]
  },
  {
    "id": "kings-birthday-2027",
    "name": "英王诞辰日长周末",
    "nameEn": "",
    "icon": "👑",
    "date": "2027-06-14",
    "month": 6,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "家庭桌游卡牌盒",
        "category": "kids",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "⚠️待复核",
        "keywords": [
          "card games family",
          "travel board games compact"
        ],
        "sourcing": "1688: 家庭桌游"
      },
      {
        "sku": "热敷眼罩(微波款)",
        "category": "wellness",
        "margin": "约54-63%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "heated eye mask microwave",
          "wheat bag eye pillow"
        ],
        "sourcing": "1688: 热敷眼罩"
      }
    ]
  },
  {
    "id": "winter-prep-2027",
    "name": "入冬准备(南半球6月冬)",
    "nameEn": "",
    "icon": "❄️",
    "date": "2027-06-01",
    "month": 6,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "热水袋针织外套装",
        "category": "wellness",
        "margin": "约53-62%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 litre",
        "keywords": [
          "hot water bottle cover knit",
          "hot water bag 2 litre"
        ],
        "sourcing": "1688: 热水袋连套"
      },
      {
        "sku": "门窗密封条自粘",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "door draft excluder strip",
          "weather stripping door"
        ],
        "sourcing": "1688: 门窗密封条"
      },
      {
        "sku": "加绒触屏手套(配件)",
        "category": "apparel",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "touchscreen gloves womens thermal",
          "winter gloves lined"
        ],
        "sourcing": "1688: 触屏手套"
      },
      {
        "sku": "暖手宝充电款排除→化学帖",
        "category": "wellness",
        "margin": "约56-65%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "hand warmers reusable gel",
          "pocket hand warmer"
        ],
        "sourcing": "1688: 暖手蛋凝胶"
      },
      {
        "sku": "室内加湿替代—蒸发水盘",
        "category": "home",
        "margin": "约54-63%",
        "matchScore": 3,
        "riskNote": "⚠️待复核 ceramic",
        "keywords": [
          "ceramic humidifier passive",
          "water dish evaporator"
        ],
        "sourcing": "1688: 陶瓷蒸发皿"
      }
    ]
  },
  {
    "id": "christmas-in-july-2027",
    "name": "七月圣诞(反季营销)",
    "nameEn": "",
    "icon": "🎅",
    "date": "2027-07-25",
    "month": 7,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "冬日圣诞桌布",
        "category": "home",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "christmas tablecloth waterproof",
          "xmas table cover"
        ],
        "sourcing": "1688: 圣诞桌布"
      },
      {
        "sku": "热红酒香料球(工具)",
        "category": "home",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "mulled wine infuser",
          "spice ball tea infuser"
        ],
        "sourcing": "1688: 调味泡球"
      },
      {
        "sku": "毛线编织餐垫DIY包",
        "category": "craft",
        "margin": "约53-62%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "knitting kit beginners",
          "yarn craft kit adults"
        ],
        "sourcing": "1688: 编织材料包"
      }
    ]
  },
  {
    "id": "prime-day-au-2027",
    "name": "Prime Day AU",
    "nameEn": "",
    "icon": "📦",
    "date": "2027-07-08",
    "month": 7,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "快递拆封工具三合一",
        "category": "home",
        "margin": "约60-68%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "package opener knife",
          "box cutter safe mail"
        ],
        "sourcing": "1688: 拆箱美工刀"
      },
      {
        "sku": "电池收纳盒(空盒)",
        "category": "home",
        "margin": "约56-65%",
        "matchScore": 3,
        "riskNote": "⚠️待复核 battery",
        "keywords": [
          "battery organizer case",
          "battery storage holder"
        ],
        "sourcing": "1688: 电池收纳盒"
      }
    ]
  },
  {
    "id": "winter-school-holidays-2027",
    "name": "寒假室内季",
    "nameEn": "",
    "icon": "🧩",
    "date": "2027-06-26",
    "month": 6,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "拼图500片家庭款",
        "category": "kids",
        "margin": "约52-61%",
        "matchScore": 5,
        "riskNote": "⚠️待复核 多件套装 500pcs (≥5件, 包装易超标)",
        "keywords": [
          "jigsaw puzzles adults 500 pieces",
          "family puzzle australian scenery"
        ],
        "sourcing": "1688: 500片拼图"
      },
      {
        "sku": "儿童手工珠串套装",
        "category": "kids",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "bead kits for kids jewellery",
          "friendship bracelet kit"
        ],
        "sourcing": "1688: 儿童串珠"
      },
      {
        "sku": "桌面冰球对战游戏",
        "category": "kids",
        "margin": "约52-61%",
        "matchScore": 4,
        "riskNote": "⚠️待复核",
        "keywords": [
          "sling puck game fast",
          "foosball winner board game"
        ],
        "sourcing": "1688: 弹射对战机"
      }
    ]
  },
  {
    "id": "back-to-school-t3-2027",
    "name": "返校季Term3",
    "nameEn": "",
    "icon": "✏️",
    "date": "2027-07-26",
    "month": 7,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "午餐冰袋反复使用",
        "category": "kids",
        "margin": "约56-65%",
        "matchScore": 4,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "ice packs lunch boxes reusable",
          "slim ice pack kids"
        ],
        "sourcing": "1688: 午餐冰袋"
      },
      {
        "sku": "课本包书皮自粘",
        "category": "stationery",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "book covers school self adhesive",
          "contact paper clear books"
        ],
        "sourcing": "1688: 自粘包书膜"
      },
      {
        "sku": "水壶保温吸管盖替换",
        "category": "kids",
        "margin": "约58-67%",
        "matchScore": 3,
        "riskNote": "⚠️待复核 kids",
        "keywords": [
          "replacement straw lids kids bottle",
          "bottle brush cleaner set"
        ],
        "sourcing": "1688: 吸管杯配件"
      }
    ]
  },
  {
    "id": "late-winter-garden-2027",
    "name": "冬末修园+早春播种",
    "nameEn": "",
    "icon": "🌱",
    "date": "2027-08-15",
    "month": 8,
    "importance": "B",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "修枝剪弹簧款",
        "category": "garden",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "pruning shears small hands",
          "secateurs garden bypass"
        ],
        "sourcing": "1688: 修枝剪"
      },
      {
        "sku": "种子育苗盘可降解",
        "category": "garden",
        "margin": "约55-64%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "seedling trays biodegradable",
          "seed starter kit peat pots"
        ],
        "sourcing": "1688: 育苗盆可降解"
      },
      {
        "sku": "植物标签牌竹制",
        "category": "garden",
        "margin": "约59-68%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "plant labels bamboo",
          "garden markers tags"
        ],
        "sourcing": "1688: 竹制植物标牌"
      },
      {
        "sku": "室内绿植吊盆",
        "category": "garden",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "hanging planters macrame",
          "indoor plant hanger basket"
        ],
        "sourcing": "1688: 吊盆编织"
      }
    ]
  },
  {
    "id": "fathers-day-au-2027",
    "name": "父亲节(澳洲9月)",
    "nameEn": "",
    "icon": "🔧",
    "date": "2027-09-05",
    "month": 9,
    "importance": "A",
    "category": "festival",
    "themeColor": "#3b82f6",
    "products": [
      {
        "sku": "多功能腰挂工具钳",
        "category": "gift",
        "margin": "约51-60%",
        "matchScore": 5,
        "riskNote": "",
        "keywords": [
          "multi tool pliers compact",
          "gifts for dad tools"
        ],
        "sourcing": "1688: 多功能组合钳"
      },
      {
        "sku": "洗车细节刷套装",
        "category": "auto",
        "margin": "约53-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "car detailing brushes interior",
          "wheel cleaning brush set"
        ],
        "sourcing": "1688: 洗车细节刷"
      },
      {
        "sku": "烧烤温度计(机械)",
        "category": "gift",
        "margin": "约55-64%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "meat thermometer dial instant read",
          "bbq thermometer stainless"
        ],
        "sourcing": "1688: 烤肉温度计"
      },
      {
        "sku": "户外折叠椅轻量",
        "category": "outdoor",
        "margin": "约48-56%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "lightweight folding chair backpacking",
          "compact camp chair heavy duty"
        ],
        "sourcing": "1688: 超轻折叠椅"
      }
    ]
  },
  {
    "id": "afterpay-day-mar-2027",
    "name": "Afterpay Day(3月场)",
    "nameEn": "Afterpay Day March",
    "icon": "💳",
    "date": "2027-03-19",
    "month": 3,
    "importance": "B",
    "category": "festival",
    "themeColor": "#b8b8ff",
    "products": [
      {
        "sku": "折叠桌面收纳盒",
        "category": "home",
        "margin": "约52-62%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "desk organiser foldable",
          "storage box office"
        ],
        "sourcing": "1688: 折叠桌面收纳盒"
      },
      {
        "sku": "行李箱收纳七件套(轻量)",
        "category": "home",
        "margin": "约50-60%",
        "matchScore": 3,
        "riskNote": "⚠️待复核 套装件数与包装尺寸",
        "keywords": [
          "packing cubes luggage organiser"
        ],
        "sourcing": "1688: 行李箱收纳套装"
      }
    ]
  },
  {
    "id": "click-frenzy-mayhem-2027",
    "name": "Click Frenzy Mayhem(5月)",
    "nameEn": "Click Frenzy Mayhem May",
    "icon": "⚡",
    "date": "2027-05-14",
    "month": 5,
    "importance": "B",
    "category": "festival",
    "themeColor": "#7c3aed",
    "products": [
      {
        "sku": "桌面线缆收纳夹条",
        "category": "home",
        "margin": "约55-65%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "cable organiser desk clip",
          "cord management"
        ],
        "sourcing": "1688: 硅胶理线器"
      },
      {
        "sku": "野餐保温袋(小号)",
        "category": "gift",
        "margin": "约48-58%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "lunch bag insulated small",
          "picnic cooler bag"
        ],
        "sourcing": "1688: 保温午餐包"
      }
    ]
  },
  {
    "id": "afterpay-day-aug-2027",
    "name": "Afterpay Day(8月场)",
    "nameEn": "Afterpay Day August",
    "icon": "💳",
    "date": "2027-08-20",
    "month": 8,
    "importance": "B",
    "category": "festival",
    "themeColor": "#b8b8ff",
    "products": [
      {
        "sku": "冰箱侧挂收纳袋",
        "category": "home",
        "margin": "约50-60%",
        "matchScore": 4,
        "riskNote": "",
        "keywords": [
          "fridge side organizer",
          "magnetic fridge storage"
        ],
        "sourcing": "1688: 冰箱侧挂收纳"
      },
      {
        "sku": "编织手提购物包",
        "category": "apparel",
        "margin": "约55-65%",
        "matchScore": 3,
        "riskNote": "",
        "keywords": [
          "woven tote bag market",
          "straw handbag"
        ],
        "sourcing": "1688: 编织手提包"
      }
    ]
  }
];