#!/usr/bin/env python3
"""
Seed Demo Data for Diesel Industry Hub
Creates mock news posts, documents, and comments
"""

import os
import sys
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import random
import string
import json

def generate_id():
    """Generate a unique ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=21))

def seed_data(db_url):
    """Seed demo data"""
    
    print("\n" + "="*60)
    print("  🌱 Seeding Demo Data - Diesel Industry Hub")
    print("="*60 + "\n")
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Get first user (will be the owner of posts)
    cur.execute("SELECT id, name FROM users ORDER BY \"createdAt\" LIMIT 1")
    user_row = cur.fetchone()
    if not user_row:
        print("❌ No users found! Please sign up first.")
        return
    
    user_id = user_row[0]
    user_name = user_row[1] or "Admin"
    
    print(f"📝 Creating content as: {user_name}\n")
    
    # Check if we already have posts
    cur.execute("SELECT COUNT(*) FROM posts")
    existing_posts = cur.fetchone()[0]
    
    if existing_posts > 0:
        print(f"⚠️  Found {existing_posts} existing posts")
        response = input("Delete and recreate? (y/n): ")
        if response.lower() == 'y':
            cur.execute("DELETE FROM reactions WHERE \"commentableType\" = 'post'")
            cur.execute("DELETE FROM comments WHERE \"commentableType\" = 'post'")
            cur.execute("DELETE FROM posts")
            print("✅ Cleared existing posts\n")
        else:
            print("Keeping existing data\n")
            return
    
    # Mock news posts
    posts = [
        {
            'type': 'news',
            'title': '🚀 New EPA 2024 Standards for Heavy-Duty Diesel Engines',
            'content': '''The EPA has announced new emission standards that will take effect in 2024. Key changes include:

• **NOx emissions** reduced by 90% from current standards
• **Particulate matter** limits tightened significantly  
• **Extended useful life** requirements to 450,000 miles
• **New testing procedures** for real-world conditions

These changes will require significant updates to aftertreatment systems, including SCR catalysts, DPF filters, and DEF dosing strategies.

**Impact on remanufacturing:** We'll need to update our testing protocols and ensure all reman units meet these new standards.''',
            'tags': ['EPA', 'Regulations', 'Emissions', '2024'],
            'is_pinned': True,
            'external_link': 'https://www.epa.gov/regulations-emissions-vehicles-and-engines',
        },
        {
            'type': 'bulletin',
            'title': '📦 New Parts Shipment Arriving Friday',
            'content': '''Just got confirmation from our supplier - large shipment arriving this Friday:

✅ **150 turbochargers** (various models)
✅ **80 EGR coolers** (Cummins ISX)
✅ **200 injectors** (Detroit DD15)
✅ **50 high-pressure fuel pumps** (Duramax)

Please plan warehouse space accordingly. Stock will be unloaded starting 8 AM.

If you need anything from this shipment prioritized, let me know ASAP!''',
            'tags': ['Inventory', 'Shipment', 'Warehouse'],
            'is_pinned': False,
        },
        {
            'type': 'diesel_tech',
            'title': '💡 Understanding Common Rail Injection Pressure Trends',
            'content': '''Interesting trend we're seeing in modern diesel engines - injection pressures keep climbing:

**2000-2005:** 1,600 bar (23,000 PSI)
**2010-2015:** 2,000 bar (29,000 PSI)  
**2020+:** 2,500+ bar (36,000+ PSI)

**Why?** Higher pressure = better fuel atomization = cleaner combustion = lower emissions.

**Challenges:**
- More stress on injector components
- Tighter tolerances required
- More sensitive to fuel quality
- Higher costs for replacement parts

**For remanufacturing:** We need to pay extra attention to wear patterns and ensure precise calibration. Even small deviations can cause performance issues.

What pressures are you seeing in the shop?''',
            'tags': ['Common Rail', 'Fuel Systems', 'Tech Deep-Dive'],
            'is_pinned': False,
        },
        {
            'type': 'announcement',
            'title': '⚠️ DEF Quality Issues - National Alert',
            'content': '''**URGENT:** Multiple reports of contaminated DEF (Diesel Exhaust Fluid) causing SCR system failures across the country.

**Symptoms:**
- SCR efficiency codes (P20EE, P20BA)
- Crystallization in dosing modules
- Clogged DEF lines and injectors

**Affected brands:** Several off-brand suppliers (names withheld pending investigation)

**Recommendation:**
- Use only **ISO 22241-compliant DEF**
- Check DEF concentration with refractometer
- Inspect customer's DEF supply if you see SCR issues
- Document DEF brand when diagnosing failures

This could save you hours of diagnostic time. Stay alert!''',
            'tags': ['DEF', 'SCR', 'Quality Alert', 'Diagnostics'],
            'is_pinned': True,
        },
        {
            'type': 'diesel_tech',
            'title': '🔧 Turbo Failure Analysis: What We Can Learn',
            'content': '''Analyzed 50 failed turbos last month. Here's what we found:

**Top failure modes:**
1. **Oil contamination (32%)** - Dirty oil destroying bearings
2. **Compressor surge (24%)** - Improper sizing/installation
3. **Exhaust restrictions (18%)** - DPF issues causing back pressure
4. **Shaft imbalance (15%)** - FOD or manufacturing defect
5. **Other (11%)** - Various causes

**Key takeaway:** Most failures are preventable! 

✅ Regular oil changes
✅ Proper air filtration  
✅ Correct turbo sizing
✅ Monitor DPF condition

Worth sharing with customers - might save them money!''',
            'tags': ['Turbochargers', 'Failure Analysis', 'Preventive Maintenance'],
            'is_pinned': False,
        },
        {
            'type': 'bulletin',
            'title': '🎉 Shop Floor Safety Record - 100 Days!',
            'content': '''Amazing milestone team! 

**100 days without a workplace injury!** 🎊

This doesn't happen by accident. Thank you all for:
- Following safety protocols
- Wearing proper PPE
- Looking out for each other
- Reporting hazards immediately

Let's keep this streak going! Safety first, always.

Pizza party this Friday to celebrate! 🍕''',
            'tags': ['Safety', 'Team', 'Milestone'],
            'is_pinned': False,
        },
    ]
    
    print("📰 Creating news posts...")
    post_ids = []
    
    for post_data in posts:
        post_id = generate_id()
        post_ids.append(post_id)
        
        cur.execute("""
            INSERT INTO posts (
                id, type, title, content, tags, is_pinned, 
                external_link, author_id, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s)
        """, (
            post_id,
            post_data['type'],
            post_data['title'],
            post_data['content'],
            json.dumps(post_data['tags']),
            post_data['is_pinned'],
            post_data.get('external_link'),
            user_id,
            datetime.now() - timedelta(days=random.randint(0, 30)),
            datetime.now(),
        ))
        print(f"  ✅ {post_data['title'][:50]}...")
    
    print(f"\n✅ Created {len(posts)} posts\n")
    
    # Add some comments
    print("💬 Adding comments...")
    
    comments = [
        ("Great info! We've been seeing these pressure issues too.", 0),
        ("Thanks for the heads up on the DEF quality problems!", 1),
        ("Can we get specs on those new turbos?", 2),
        ("This is exactly what I needed to know!", 0),
        ("Pizza party! Count me in! 🍕", 1),
    ]
    
    for comment_text, post_idx in comments:
        if post_idx < len(post_ids):
            comment_id = generate_id()
            cur.execute("""
                INSERT INTO comments (
                    id, commentable_id, commentable_type, content,
                    author_id, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                comment_id,
                post_ids[post_idx],
                'post',
                comment_text,
                user_id,
                datetime.now() - timedelta(hours=random.randint(1, 48)),
            ))
    
    print(f"✅ Added {len(comments)} comments\n")
    
    # Add documents
    print("📚 Creating knowledge base documents...")
    
    documents = [
        {
            'title': 'Turbocharger Rebuild Procedure - Training Video',
            'category': 'training_video',
            'description': 'Step-by-step training video for rebuilding common rail turbochargers',
            'file_url': '/docs/turbo-rebuild-guide.pdf',
            'file_type': 'pdf',
            'tags': ['Turbo', 'Rebuild', 'Procedure', 'Technical'],
        },
        {
            'title': 'Common DPF Fault Codes - Quick Reference',
            'category': 'faq',
            'description': 'Quick reference guide for DPF-related fault codes and solutions',
            'file_url': '/docs/dpf-fault-codes.pdf',
            'file_type': 'pdf',
            'tags': ['DPF', 'Diagnostics', 'Fault Codes'],
        },
        {
            'title': 'Safety Data Sheet - Diesel Fuel Handling',
            'category': 'safety_guideline',
            'description': 'SDS for #2 Diesel Fuel handling and emergency procedures',
            'file_url': '/docs/diesel-fuel-sds.pdf',
            'file_type': 'pdf',
            'tags': ['Safety', 'SDS', 'Diesel Fuel'],
        },
    ]
    
    for doc_data in documents:
        doc_id = generate_id()
        
        cur.execute("""
            INSERT INTO documents (
                id, title, category, description, file_url, file_type, tags,
                uploaded_by, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s)
        """, (
            doc_id,
            doc_data['title'],
            doc_data['category'],
            doc_data['description'],
            doc_data['file_url'],
            doc_data['file_type'],
            json.dumps(doc_data['tags']),
            user_id,
            datetime.now() - timedelta(days=random.randint(0, 60)),
            datetime.now(),
        ))
        print(f"  ✅ {doc_data['title']}")
    
    print(f"\n✅ Created {len(documents)} documents\n")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("="*60)
    print("  🎉 Demo Data Seeded Successfully!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • {len(posts)} news posts")
    print(f"   • {len(comments)} comments")
    print(f"   • {len(documents)} knowledge base documents")
    print(f"   • Content created as: {user_name}")
    print("\n🚀 Refresh your app to see the new content!\n")

def main():
    print("\n" + "="*60)
    print("  🌱 Demo Data Seeder - Diesel Industry Hub")
    print("="*60 + "\n")
    
    # Get database URL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("\nTo fix this:")
        print("  1. Make sure you have a .env file")
        print("  2. Add: DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    try:
        seed_data(db_url)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

