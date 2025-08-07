# Database Schema Setup Guide

## 🎯 **Current Status**

✅ **S3 Connection**: Working perfectly!  
❌ **Database**: Schema not created yet

## 📋 **Quick Setup Steps**

### **1. Open Supabase SQL Editor**

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: `csdzhpskeyqswqmffvxv`
3. Click **"SQL Editor"** in the left sidebar
4. Click **"New Query"**

### **2. Copy and Run the Schema**

1. **Open the file**: `database_integration/is_migration_schema.sql`
2. **Copy ALL the content** (it's about 200+ lines)
3. **Paste it** into the Supabase SQL Editor
4. **Click "Run"** button

### **3. Verify Schema Creation**

After running the SQL, you should see:
- ✅ Schema `is_migration` created
- ✅ 7 tables created
- ✅ Functions and indexes created
- ✅ Row Level Security enabled

### **4. Test the Integration**

Run the test again:
```bash
python test_database_only.py
```

You should now see:
- ✅ Database: Connected
- ✅ Storage: Connected

## 🗄️ **What Gets Created**

### **Schema: `is_migration`**
All tables are isolated in this schema to avoid conflicts.

### **Tables Created:**
1. **`jobs`** - Main job tracking
2. **`documents`** - File metadata with vector search
3. **`job_history`** - Complete change tracking
4. **`user_activity`** - User action monitoring
5. **`user_feedback`** - Feedback and ratings
6. **`system_metrics`** - Analytics data
7. **`iflow_generations`** - iFlow generation tracking

### **Features Enabled:**
- ✅ Vector search with pgvector
- ✅ Row Level Security (RLS)
- ✅ Proper indexes for performance
- ✅ Foreign key relationships
- ✅ Utility functions

## 🔧 **If You Get Errors**

### **Error: "pgvector extension not found"**
1. Go to **Database > Extensions** in Supabase
2. Enable the **"vector"** extension
3. Re-run the schema script

### **Error: "Permission denied"**
1. Make sure you're using the **Service Role Key** (not anon key)
2. Check your `.env` file has `SUPABASE_SERVICE_ROLE_KEY`

### **Error: "Schema already exists"**
1. The script handles this - it will skip existing objects
2. You can safely re-run the script

## 📊 **After Setup**

Once the schema is created, your application will have:

### **Complete File Tracking**
Every XML upload will be:
- ✅ Stored in S3
- ✅ Tracked in database
- ✅ History logged
- ✅ User activity recorded

### **Analytics Ready**
- Job completion rates
- User activity patterns
- File upload statistics
- Feedback and ratings

### **Production Ready**
- Schema isolation
- Row-level security
- Proper indexing
- Error handling

## 🚀 **Next Steps After Schema Setup**

1. **Run the test**: `python test_database_only.py`
2. **Start your app**: `python app/app.py`
3. **Upload XML files** via the UI
4. **Check S3 bucket** for files
5. **Check Supabase** for database records

## 📝 **Quick Copy-Paste**

Here's the exact file to copy from:
```
database_integration/is_migration_schema.sql
```

Copy the **entire content** and paste it into Supabase SQL Editor, then click **Run**.

That's it! Your database will be ready for enterprise-grade file tracking and analytics. 🎯
