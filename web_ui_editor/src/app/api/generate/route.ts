import { NextRequest, NextResponse } from 'next/server'
import { FilterParser } from '@/lib/FilterParser'

export async function POST(request: NextRequest) {
  try {
    const { data, format } = await request.json()

    if (!data) {
      return NextResponse.json(
        { success: false, message: 'No data provided' },
        { status: 400 }
      )
    }

    const parser = new FilterParser()
    let content

    switch (format) {
      case 'filter':
        content = parser.generateFilterContent(data)
        break
      case 'json':
        content = JSON.stringify(data, null, 2)
        break
      case 'yaml':
        content = generateYamlContent(data)
        break
      default:
        return NextResponse.json(
          { success: false, message: 'Unsupported format' },
          { status: 400 }
        )
    }

    return NextResponse.json({
      success: true,
      content,
      filename: `${data.name || 'filter'}.${format}`
    })
  } catch (error) {
    return NextResponse.json(
      { 
        success: false, 
        message: `Error generating content: ${(error as Error).message}` 
      },
      { status: 500 }
    )
  }
}

function generateYamlContent(data: any): string {
  let yaml = `name: ${data.name || 'Custom Filter'}\n`
  yaml += `platform: ${data.platform || 'pc'}\n`
  yaml += `soundType: ${data.soundType || 'type-01'}\n`
  yaml += `rules:\n`

  data.rules.forEach((rule: any) => {
    yaml += `  - id: ${rule.id}\n`
    yaml += `    show_hide: ${rule.show_hide}\n`
    yaml += `    comment: ${rule.comment || 'No comment'}\n`
    yaml += `    enabled: ${rule.enabled}\n`
    yaml += `    conditions:\n`
    
    rule.conditions.forEach((condition: any) => {
      yaml += `      - type: ${condition.type}\n`
      yaml += `        operator: ${condition.operator}\n`
      yaml += `        values: [${condition.values.map((v: any) => `"${v}"`).join(', ')}]\n`
    })

    yaml += `    actions:\n`
    rule.actions.forEach((action: any) => {
      yaml += `      - type: ${action.type}\n`
      yaml += `        values: [${action.values.map((v: any) => `"${v}"`).join(', ')}]\n`
    })
  })

  return yaml
}

export async function GET() {
  return NextResponse.json({
    message: 'Filter Generator API',
    version: '1.0.0',
    supportedFormats: ['filter', 'json', 'yaml']
  })
}
