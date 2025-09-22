import { NextRequest, NextResponse } from 'next/server'
import { FilterParser } from '@/lib/FilterParser'

export async function POST(request: NextRequest) {
  try {
    const { content, format } = await request.json()

    if (!content) {
      return NextResponse.json(
        { success: false, message: 'No content provided' },
        { status: 400 }
      )
    }

    const parser = new FilterParser()
    let result

    switch (format) {
      case 'filter':
        result = parser.parseFilterFile(content)
        break
      case 'json':
        result = JSON.parse(content)
        break
      default:
        return NextResponse.json(
          { success: false, message: 'Unsupported format' },
          { status: 400 }
        )
    }

    return NextResponse.json({
      success: true,
      data: result
    })
  } catch (error) {
    return NextResponse.json(
      { 
        success: false, 
        message: `Error parsing content: ${(error as Error).message}` 
      },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Filter Parser API',
    version: '1.0.0',
    endpoints: {
      'POST /api/parse': 'Parse filter content',
      'POST /api/generate': 'Generate filter content'
    }
  })
}
